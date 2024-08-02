# from flask import request, jsonify, current_app
# from flask_mail import Mail, Message
# from concert_mailer.auth import login_required

# import logging

# from concert_mailer import app
# from concert_mailer.db import get_concert, update_concert


# current_app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USERNAME='coleparksphotography@gmail.com',
#     MAIL_PASSWORD='6JAT4-8X00H-L7MFN-94T68-4NG5P1'
# )

# mail = Mail(app)

# @app.route('/send_email/<int:concert_id>', methods=['POST'])
# @login_required
# def send_concert_email(concert_id):
#     data = request.json
#     message = data['message']
    
#     concert = get_concert(concert_id)
#     if concert is None:
#         return jsonify({'success': False, 'message': 'Concert not found'}), 404

#     try:
#         msg = Message(subject='Concert Information',
#                       recipients=[concert['mgmt_email']],
#                       body=message)
#         mail.send(msg)
#         # Optionally, update the emailed status
#         update_concert(concert_id, concert['date'], concert['artist'], concert['venue'], concert['mgmt_email'], concert['mgmt_name'], emailed=True)
#         return jsonify({'success': True})
#     except Exception as e:
#         print(e)
#         return jsonify({'success': False, 'message': str(e)}), 500