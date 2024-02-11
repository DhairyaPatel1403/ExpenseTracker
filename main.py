import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")


if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'budgets' not in st.session_state:
    st.session_state.budgets = {
        'Food': 2000,
        'Household': 15000,
        'Digital/Electronics': 50000,
        'Extra': 10000
    }
 

st.title(''' Expense :blue[Manager] ''')

colmain, colvalset=st.columns(2)

with colmain:

    expense = ""
    spend = ""
    expense_type = ""

    with st.container():
        col1, col2, col3 = st.columns(3) 

        with col1:
            expense = st.text_input("Enter your new expense.", value="", key=len(st.session_state.expenses)+1)
        with col2:
            spend = st.text_input('Input the amount.', value="", key=len(st.session_state.expenses)+2)
        with col3:  
            expense_type = st.selectbox('What is the type of expense?', ["Household", "Digital/Electronics", "Food", "Extra"], index=0)

    if st.button('Add Expense'):

        if expense != "" and spend != "" and expense_type != "" and spend.isdigit():
            spend = int(spend)

            expense_details = f"{len(st.session_state.expenses)+1},{expense},{spend},{expense_type}"
            st.session_state.expenses.append(expense_details)
            st.experimental_rerun()
        else:
            st.warning('All fields should be filled and Spent amount should be a number')

    if len(st.session_state.expenses) != 0:
        expense_list = []
        for i, item in enumerate(st.session_state.expenses, start=1):
            # Split each expense detail string to retrieve individual pieces of information
            expense_data = item.split(',')
            if len(expense_data) == 4:  # Ensure that there are four elements in the split result
                expense_id, expense_name, expense_spend, expense_type = expense_data
                comment=""
                expense_spend=int(expense_spend)
                if((expense_spend)>(st.session_state.budgets[expense_type])):
                    comment="Going to high here."
                elif((expense_spend)>(st.session_state.budgets[expense_type])):
                    comment="Going to high here."
                elif((expense_spend)>(st.session_state.budgets[expense_type])):
                    comment="Going to high here."
                elif((expense_spend)>(st.session_state.budgets[expense_type])):
                    comment="Going to high here."
                else:
                    comment="Good spending!"
                expense_dict = {
                    'ID': expense_id,
                    'Name': expense_name,
                    'Spend': expense_spend,
                    'Type': expense_type,
                    'Comments': comment
                }
                expense_list.append(expense_dict)
            else:
                st.warning(f"Invalid format for expense at index {i}: {item}")


        # Create DataFrame from list of dictionaries
        expenses_df = pd.DataFrame(expense_list)
        st.write(expenses_df)

    else:
        st.info('No expenses today !!!')

    st.header("Your expense in each category.")


with colvalset:
    st.write("Set the budget values yourself [By Default are set as per avg Indian Budget]")

    for category in st.session_state.budgets:
        st.session_state.budgets[category] = st.number_input(f'Budget for {category}', value=st.session_state.budgets[category])


st.header('Total Expenses by Category')
category_totals = {category: 0 for category in st.session_state.budgets}

for expense in st.session_state.expenses:
    expense_data = expense.split(',')
    if len(expense_data) == 4:
        expense_category = expense_data[3]
        expense_amount = int(expense_data[2])
        category_totals[expense_category] += expense_amount

for category, total in category_totals.items():
    st.write(f"{category}: {total}")
    if total > st.session_state.budgets[category]:
        st.warning(f"Total expenses for {category} exceed the budget!")

# Create a bar chart for total expenses
st.header('Bar Chart of Total Expenses [Click on 3 dots on right top for more options]')
st.bar_chart(category_totals)