import csv
import io

import pandas as pd
import streamlit as st


def _report_as_csv(records, headers):
    """Return report rows as UTF-8 CSV bytes for a download button."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue().encode("utf-8")


def show_finance_page(manager):
    """Render payment recording, history, and report downloads."""
    st.header("Finance & Payments")

    student_options = {
        f"{student.name} (ID: {student.id})": student.id
        for student in manager.students
    }

    if not student_options:
        st.warning("Register at least one student before recording payments.")
        return

    st.subheader("Record New Payment")
    with st.form("payment_form", clear_on_submit=True):
        student_label = st.selectbox(
            "Select Student", student_options.keys(), key="payment_student"
        )
        amount = st.number_input(
            "Payment Amount ($)", min_value=0.01, step=1.0, format="%.2f"
        )
        method = st.selectbox(
            "Payment Method", ["Cash", "Credit Card", "Bank Transfer"]
        )
        submitted = st.form_submit_button("Record Payment")

        if submitted:
            success = manager.record_payment(
                student_options[student_label], amount, method
            )
            if success:
                st.success(
                    f"Payment of ${amount:.2f} recorded for {student_label}."
                )
            else:
                st.error("Payment could not be recorded. Check the details.")

    st.divider()
    st.subheader("Student Payment History")
    with st.form("payment_history_form"):
        history_label = st.selectbox(
            "Select Student", student_options.keys(), key="history_student"
        )
        view_history = st.form_submit_button("View Payment History")

        if view_history:
            history = manager.get_payment_history(
                student_options[history_label]
            )

            if history:
                history_table = pd.DataFrame(history).rename(
                    columns={
                        "student_id": "Student ID",
                        "amount": "Amount ($)",
                        "method": "Method",
                        "timestamp": "Timestamp",
                    }
                )
                st.dataframe(history_table, width="stretch", hide_index=True)
                total_paid = sum(payment["amount"] for payment in history)
                st.metric("Total Paid", f"${total_paid:.2f}")
            else:
                st.info("This student has no payment history.")

    st.divider()
    st.subheader("Download Reports")
    finance_column, attendance_column = st.columns(2)

    finance_column.download_button(
        "Download Finance CSV",
        data=_report_as_csv(
            manager.finance_log,
            ["student_id", "amount", "method", "timestamp"],
        ),
        file_name="finance_report.csv",
        mime="text/csv",
    )
    attendance_column.download_button(
        "Download Attendance CSV",
        data=_report_as_csv(
            manager.attendance_log,
            ["student_id", "course_id", "timestamp"],
        ),
        file_name="attendance_report.csv",
        mime="text/csv",
    )
