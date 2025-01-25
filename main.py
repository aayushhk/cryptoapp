
import streamlit as st
import requests
import json
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
import os


st.set_page_config("TxnTracker","🤖",layout="wide")
# Initialize the FirecrawlApp with your API key

API_KEY = os.getenv('FIRECRAWL_API_KEY', 'fc-c903b7b1acfb436aa42d06df1d67ed84')

if not API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY environment variable is not set.")

app_instance = FirecrawlApp(api_key=API_KEY)

class ExtractSchema(BaseModel):
    wallet_address:str
    eth_balance: str
    eth_value: str
    token_holdings:str
    latest_transaction_sent:str
    first_transaction_sent:str
    multichain_portfolio_balance: str
    public_name_tag:str
class ExtractSchematx(BaseModel):
    transaction_hash:str
    transaction_from:str
    transaction_from_platform_app:str
    transaction_to:str
    transaction_to_platform_app:str
    amount_in_usd:str
    transaction_block_number:str
    transaction_timestamp:str
    transaction_gas_used:str
    transaction_gas_limit:str
    transaction_input:str
    transaction_output:str
    transaction_contract_address:str  



  

def scrape(bc, tx_hash,q,schem):
    if bc == "eth":
        bc_url = 'https://etherscan.io'
    elif bc == "bnb":
        bc_url = 'https://bscscan.com'
    else:
        raise ValueError("Unsupported blockchain")

    etherscan_link = f'{bc_url}/{q}/{tx_hash}'

    data = app_instance.scrape_url(etherscan_link, {
        'formats': ['extract'],
        'extract': {
            'schema': schem.model_json_schema(),
        }
    })
    return data
def main():
    col1,col2=st.columns(2)
    with col1:
        tab1,tab2=st.tabs(["tab1", "tab2"])
        # Input field for addx
        with tab1:
            addx = st.text_input("Enter Wallet Address (addx):", placeholder="0x...")

            # Radio button for bc
            bc = st.radio("Select Blockchain (bc):", options=["eth", "bsc"], index=0,key="addK")
            execu=st.button("Fetch info",key="addB",type="primary")

        with tab2:
            addxc = st.text_input("Enter Transaction hash:", placeholder="0x...")
            # Radio button for bc
            bcc = st.radio("Select Blockchain (bc):", options=["eth", "bsc"], index=0,key="hashK")
            execuc=st.button("Fetch info",key="hashB",type="primary")
            # Button to fetch data
    with col2:    
        if execu:
            if not addx:
                st.error("Please enter a valid wallet address.")
            else:
                # Call the API
            
                try:
                    response = scrape(bc,addx,"address",ExtractSchema)

                    data = response

                    # Display the result in a user-friendly format
                    if "extract" in data:
                        with st.container(border=True):
                            result = data["extract"]
                            st.caption("Wallet Address")
                            st.code(result.get('wallet_address', 'N/A'))

                            st.caption("ETH Balance")
                            st.write(result.get('eth_balance', 'N/A'))

                            st.caption("ETH Value")
                            st.write(result.get('eth_value', 'N/A'))

                            st.caption("First Transaction Sent")
                            st.write(result.get('first_transaction_sent', 'N/A'))

                            st.caption("Latest Transaction Sent")
                            st.write(result.get('latest_transaction_sent', 'N/A'))

                            st.caption("Multichain Portfolio Balance")
                            st.write(result.get('multichain_portfolio_balance', 'N/A'))

                            st.caption("Public Name Tag")
                            st.write(result.get('public_name_tag', 'N/A'))

                            st.caption("Token Holdings")
                            st.write(result.get('token_holdings', 'N/A'))

                    else:
                        st.error("Unexpected response format.")
                  
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred while calling the API: {e}")
        if execuc:
            if not addxc:
                st.error("Please enter a valid transaction hash.")
            else:
                # Call the API
            
                try:
                    response = scrape(bcc,addxc,"tx",ExtractSchematx)
                    
                    data = response

                    # Display the result in a user-friendly format
                    if "extract" in data:
                        with st.container(border=True):
                            result = data["extract"]
                            st.caption("Transaction Hash")
                            st.code(result.get('transaction_hash', 'N/A'))

                            st.caption("Transaction From")
                            st.code(result.get('transaction_from', 'N/A'))

                            st.caption("Transaction From Platform App")
                            st.code(result.get('transaction_from_platform_app', 'N/A'))

                            st.caption("Transaction To")
                            st.code(result.get('transaction_to', 'N/A'))

                            st.caption("Transaction To Platform App")
                            st.code(result.get('transaction_to_platform_app', 'N/A'))

                            st.caption("Amount in USD")
                            st.code(result.get('amount_in_usd', 'N/A'))

                            st.caption("Transaction Block Number")
                            st.code(result.get('transaction_block_number', 'N/A'))

                            st.caption("Transaction Timestamp")
                            st.code(result.get('transaction_timestamp', 'N/A'))

                            st.caption("Transaction Gas Used")
                            st.code(result.get('transaction_gas_used', 'N/A'))

                            st.caption("Transaction Gas Limit")
                            st.code(result.get('transaction_gas_limit', 'N/A'))

                            st.caption("Transaction Input")
                            st.code(result.get('transaction_input', 'N/A'))

                            st.caption("Transaction Output")
                            st.code(result.get('transaction_output', 'N/A'))

                            st.caption("Transaction Contract Address")
                            st.code(result.get('transaction_contract_address', 'N/A'))
                    else:
                        st.error("Unexpected response format.")
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred while calling the API: {e}")

if __name__ == "__main__":
    main()
