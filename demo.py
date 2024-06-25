import openai
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.prompts.chat import MessagesPlaceholder
import os
import ipywidgets as widgets
from IPython.display import display, clear_output
from langchain.agents import create_openai_tools_agent, AgentExecutor
from dotenv import load_dotenv
from difflib import ndiff
from IPython.display import HTML

# Importing required tools
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

tools = [add, multiply]

# Add your env file
load_dotenv(r"***************")

# Set up Azure OpenAI LLM
llm = AzureChatOpenAI( 
    openai_api_key=os.getenv("KEY"),
    azure_endpoint=os.getenv("ENDPOINT"),
    openai_api_version=os.getenv("API_VERSION"),
    deployment_name=os.getenv("LLM_MODEL_NAME"),
    temperature=0,
)

# Original contract
original_contract = """
RENTAL AGREEMENT
This RENTAL AGREEMENT is executed at Kolkatta on this  5 day of July, 2023by and between: 
XYZ Pvt Ltd., 
15/7 DH road Kolkata, 700017
(hereinafter jointly and severally called the “OWNER”, which expression shall include their heirs, legal representatives, successors and assigns) of the ONE PART:
AND, in favour of:
ABC Pvt Ltd, 
Working/Studying at 79H PQR road Kolkatta 700092
having a permanent address at Hoogly road 21003
(hereinafter called the “TENANT”, which expression shall include its legal representatives, successors and assigns) of the OTHER PART.
WHEREAS the Owner is the absolute owner of the property situated at 114/34 sec2 kolkatta 700142 as detailed in Annexure-I, hereinafter referred to as "Demised Premises".
WHEREAS the Tenant has requested the Owner to grant Rent with respect to the Schedule Premises and the Owner has agreed to rent out to the Tenant the Property with two-wheeler and four-wheeler parking space in the ground floor for residential purposes only, on the following terms and conditions:
NOW THIS DEED WITNESSETH AS FOLLOWS:
1. The rent in respect of the “Demised Premises” shall commence from (10 July 2023) and shall be valid till (10 December 2024). Thereafter, the same may be extended further on mutual consent of both the parties.
2. That the Tenant shall pay to the Owner a monthly rent of Rs.(20,000), excluding electricity and water bill. The rent shall be paid on or before 7th day of each month without fail.
3. That the Tenant shall pay to the Owner a monthly maintenance charge of Rs.5,000 towards the maintenance of Generator & Elevator, Salaries towards guards, Charges for Electricity Maintenance for Common Areas, Charges towards cleaning of Common Areas and towards maintaining the lawn.
4. That the Tenant shall pay for the running cost of elevator and generator separately to the Owner.
5. That during the Rent period, in addition to the rental amount payable to the Owner, the Tenant shall pay for the use of electricity and water as per bills received from the authorities concerned directly. For all the dues of electricity bills and water bills till the date the possession of the premises is handed over by the Owner to the Tenant it is the responsibility of the Owner to pay and clear them according to the readings on the respective meters. At the time of handing over possession of the premises back to the Owner by Tenant, it is the responsibility of the Tenant to pay electricity & water bills, as presented by the Departments concerned according to the readings on the respective meters upto the date of vacation of the property.
6. The Tenant will pay to the Owner an interest-free refundable security deposit of Rs.(70,000) vide cheque no (12347ZY) dated (9 july 2023) at the time of signing the Rent Agreement. The said amount of the Security deposit shall be refunded by the Owner to the Tenant at the time of handing over possession of the demised premises by the Tenant upon expiry or sooner termination of this Rent after adjusting any dues (if any) or cost towards damages caused by the negligence of the Tenant or the person he is responsible for, normal wear & tear and damages due to act of god exempted. In case the Owner fails to refund the security deposit to the Tenant on early termination or expiry of the Rent agreement, the Tenant is entitled to hold possession of the Rented premises, without payment of rent and/or any other charges whatsoever, till such time the Owner refunds the security deposit to the Tenant. This is without prejudice and in addition to the other remedies available to the Tenant to recover the amount from the Owner.
7. That all the sanitary, electrical and other fittings and fixtures and appliances in the premises shall be handed over from the Owner to the Tenant in good working condition. 
8. That the Tenant shall not sublet, assign or part with the demised premises in whole or part thereof to any person in any circumstances whatsoever and the same shall be used for the bonafide residential purposes only.
9. That the day-to-day minor repairs will be the responsibility for the Tenant at his/her own expense. However, any structural or major repairs, if so required, shall be carried out by the Owner.
10. That no structural additions or alterations shall be made by the Tenant in the premises without the prior written consent of the Owner but the Tenant can install air-conditioners in the space provided and other electrical gadgets and make such changes for the purposes as may be necessary, at his own cost. On termination of the tenancy or earlier, the Tenant will be entitled to remove such equipment and restore the changes made, if any, to the original state.
11. That the Owner shall hold the right to visit in person or through his authorized agent(s), servants, workmen etc., to enter upon the demised premises for inspection (not exceeding once in a month) or to carry out repairs / construction, as and when required.
12. That the Tenant shall comply with all the rules and regulations of the local authority applicable to the demised premises. The premises will be used only for residential purposes of its employees, families and guests.
13. That the Owner shall pay for all taxes/cesses levied on the premises by the local or government authorities in the way of property tax for the premises and so on. Further, any other payment in the nature of subscription or periodical fee to the welfare association shall be paid by the Owner.
14. That the Owner will keep the Tenant free and harmless from any claims, proceedings, demands, or actions by others with respect to quiet possession of the premises.
15. That this Rent Agreement can be terminated before the expiry of this tenancy period by serving One month prior notice in writing by either party.
16. The Tenant shall maintain the Demised Premises in good and tenable condition and all the minor repairs such as leakage in the sanitary fittings, water taps and electrical usage etc. shall be carried out by the Tenant. That it shall be the responsibility of the Tenant to hand over the vacant and peaceful possession
"""

sys_prom = "you are a helpful AI assistant which modifys the contracts based on given instructions"
messages = [
    SystemMessagePromptTemplate.from_template(sys_prom),
    HumanMessagePromptTemplate.from_template("{original_contract},{instructions}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]

prompt = ChatPromptTemplate.from_messages(messages)

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
    return_source_documents=True
)

# Function to update contract
def update_contract(original, instructions):
    try:
        response = agent_executor.invoke({"original_contract": original, "instructions": instructions})
        updated_contract = response['output']
    except Exception as e:
        updated_contract = f"Error: {str(e)}"
    return updated_contract

# Function to approve contract
def approve_contract(b):
    with output:
        clear_output()
        output.append_stdout("Contract approved and finalized.\n")
        approved_textarea.value = edit_textarea.value

# Function to edit contract
def edit_contract(b):
    with output:
        clear_output()
        output.append_stdout("Please edit the updated contract manually.\n")
        edit_textarea.value = updated_textarea.value

# Function to handle contract update based on user input
def handle_update_contract(b):
    global updated_contract
    instructions = instructions_textarea.value
    updated_contract = update_contract(original_contract, instructions)
    highlighted_contract = highlight_changes(original_contract, updated_contract)
    updated_textarea.value = updated_contract
    updated_html.value = highlighted_contract
    with output:
        clear_output()
        output.append_stdout("Contract has been updated based on the provided instructions.\n")

# Function to save manually edited contract
def save_edits(b):
    with output:
        clear_output()
        output.append_stdout("Manual edits have been saved.\n")

# Function to highlight changes in the contract
def highlight_changes(original, updated):
    diff = ndiff(original.splitlines(keepends=True), updated.splitlines(keepends=True))
    html_diff = ''
    for line in diff:
        if line.startswith('+ '):
            html_diff += f'<span style="color:green;">{line[2:]}</span>'
        elif line.startswith('- '):
            html_diff += f'<span style="color:red;">{line[2:]}</span>'
        else:
            html_diff += line[2:]
    return f'<pre>{html_diff}</pre>'

# Create and arrange widgets
header = widgets.HTML("<h2>Contract Modification Assistant</h2>")
instructions_label = widgets.HTML("<b>Instructions:</b> Provide detailed instructions to modify the contract below.")
instructions_textarea = widgets.Textarea(placeholder='Enter instructions here...', layout=widgets.Layout(width='100%', height='150px'))

original_label = widgets.HTML("<b>Original Contract:</b>")
original_textarea = widgets.Textarea(value=original_contract, layout=widgets.Layout(width='100%', height='150px'), disabled=True)

update_button = widgets.Button(description="Update Contract", button_style='primary')
update_button.on_click(handle_update_contract)

updated_label = widgets.HTML("<b>Updated Contract:</b>")
updated_textarea = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'), disabled=True)

updated_html = widgets.HTML()

approval_button = widgets.Button(description="Approve", button_style='success')
edit_button = widgets.Button(description="Edit Manually", button_style='warning')
save_edits_button = widgets.Button(description="Save Edits", button_style='info')

approval_button.on_click(approve_contract)
edit_button.on_click(edit_contract)
save_edits_button.on_click(save_edits)

approved_label = widgets.HTML("<b>Approved Contract after Editing:</b>")
approved_textarea = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'), disabled=True)

edit_label = widgets.HTML("<b>Edited Contract:</b>")
edit_textarea = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'))

output = widgets.Output()

# Layout design
layout = widgets.VBox([
    header,
    widgets.VBox([
        instructions_label,
        instructions_textarea,
        original_label,
        original_textarea,
        update_button,
        updated_label,
        updated_textarea,
        updated_html,
        widgets.HBox([edit_button, save_edits_button, approval_button]),
        output,
        approved_label,
        approved_textarea,
        edit_label,
        edit_textarea
    ], layout=widgets.Layout(border='1px solid lightgray', padding='10px', border_radius='10px'))
])

# Display the layout    
display(layout)
