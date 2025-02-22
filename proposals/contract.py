import streamlit as st
import datetime
from pdf_generator import generate_proposal

def render_contract_form():
    st.header("IT Consultation Contract")
    
    # Client Information
    st.subheader("Client Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
    with col2:    
        country = st.text_input("Country")
        proposal_date = st.date_input("Contract Date")
        validity_date = st.date_input("Validity Date", 
                                    value=proposal_date + datetime.timedelta(days=365),
                                    min_value=proposal_date)

    # Contract Details
    st.subheader("Contract Details")
    col1, col2 = st.columns(2)
    with col1:
        consultation_price = st.number_input("Consultation Fee", min_value=0.0, step=0.01)
        implementation_price = st.number_input("Implementation Fee", min_value=0.0, step=0.01)
    with col2:
        support_price = st.number_input("Support Fee", min_value=0.0, step=0.01)
        additional_price = st.number_input("Additional Services", min_value=0.0, step=0.01)

    # Calculate total
    total_price = consultation_price + implementation_price + support_price + additional_price

    # Display total
    st.subheader(f"Total Contract Value: ${total_price:,.2f}")

    if st.button("Generate Contract"):
        if not client_name:
            st.error("Please enter client name")
            return
            
        replacements = {
            "{client_name}": client_name,
            "{Email_address}": email,
            "{Phone_no}": phone,
            "{country_name}": country,
            "{date}": proposal_date.strftime("%d/%m/%Y"),
            "{validity_date}": validity_date.strftime("%d/%m/%Y"),
            "{Consultation price}": f"$ {consultation_price:,.2f}",
            "{Implementation price}": f"$ {implementation_price:,.2f}",
            "{Support price}": f"$ {support_price:,.2f}",
            "{Additional}": f"$ {additional_price:,.2f}",
            "{Total amount}": f"$ {total_price:,.2f}"
        }
        
        try:
            result = generate_proposal("IT Consultation", client_name, replacements)
            
            if result is not None:
                # Always show DOCX download
                if "docx" in result:
                    docx_data, docx_name, docx_mime = result["docx"]
                    st.download_button(
                        label="Download DOCX",
                        data=docx_data,
                        file_name=docx_name,
                        mime=docx_mime
                    )
                
                # Show PDF download if available
                if result.get("pdf"):
                    pdf_data, pdf_name, pdf_mime = result["pdf"]
                    st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=pdf_name,
                        mime=pdf_mime
                    )
            else:
                st.error("Failed to generate proposal. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
