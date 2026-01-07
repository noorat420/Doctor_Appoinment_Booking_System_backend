import resend
from flask import current_app

resend.api_key = None  # set dynamically
def send_appointment_confirmation(
    to_email: str,
    doctor_name: str,
    doctor_specialization: str,
    date: str,
    start_time: str,
    end_time: str
):
    resend.api_key = current_app.config["RESEND_API_KEY"]
    from_email = current_app.config["FROM_EMAIL"]

    try:
        resend.Emails.send({
            "from": from_email,
            "to": to_email,
            "subject": "Appointment Confirmed",
            "html": f"""
                <h3>Your appointment is confirmed</h3>
                <p><strong>Doctor:</strong> {doctor_name}</p>
                <p><strong>Specialization:</strong> {doctor_specialization}</p>
                <p><strong>Date:</strong> {date}</p>
                <p><strong>Time:</strong> {start_time} - {end_time}</p>
            """
        })
    except Exception as e:
        # Log later (never crash booking)
        print("Email failed:", str(e))



# send appointment cancellation
def send_appointment_cancellation(
    to_email: str,
    recipient_name: str,
    doctor_name: str,
    doctor_specialization: str,
    date: str,
    start_time: str,
    end_time: str,
    cancelled_by: str
):
    resend.api_key = current_app.config["RESEND_API_KEY"]

    try:
        resend.Emails.send({
            "from": current_app.config["FROM_EMAIL"],
            "to": to_email,
            "subject": "Appointment Cancelled",
            "html": f"""
                <h2>Appointment Cancelled</h2>
                <p>Hello {recipient_name},</p>
                <p>Your appointment has been cancelled.</p>
                <p><strong>Doctor:</strong> {doctor_name}</p>
                <p><strong>Specialization:</strong> {doctor_specialization}</p>
                <p><strong>Date:</strong> {date}</p>
                <p><strong>Time:</strong> {start_time} - {end_time}</p>
                <p><strong>Cancelled by:</strong> {cancelled_by}</p>
            """
        })
    except Exception as e:
        print("❌ Cancellation email failed:", str(e))
