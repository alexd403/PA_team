from email.message import EmailMessage
import ssl # !Seguridad
import smtplib #Manda el mensaje


# * Variables de entorno
def send_email(correo):
    server = "servermexicoupiitos@gmail.com"
    password = "legy sxcx mjip xphi"
    
    receptor = correo

    asunto = "Bienvenido a Mesenger Upiitos"
    cuerpo = """
    Te has registrado en Upiitos.
    """
    em = EmailMessage()
    em['From'] = server
    em['To'] = receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)
    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(server, password)
        smtp.sendmail(server, receptor, em.as_string())

