import streamlit as st
import pandas as pd

import pdfkit
from datetime import datetime
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")


st.set_page_config(page_title="Rapport de mise en service",page_icon="🧊")
st.title("Rapport de mise en service")
st.header("Informations de base")
info_base = {}
with st.expander("Informations sur le site"):
    info_base["N° de la machine"] = st.text_input("N° de la machine")
    info_base["Adresse de l'installation"] = st.text_input("Adresse de l'installation")
    info_base["Utilisateur"] = st.text_input("Utilisateur")
    info_base["Date de mise en service"] = st.date_input("Date de mise en service").strftime("%d/%m/%Y")
    info_base["FF"] = st.text_input("FF")
    info_base["Huile"] = st.text_input("Huile")
with st.expander("Informations sur l'installateur"):
    info_base["Nom du Technicien"] = st.text_input("Nom du Technicien")
    info_base["N° de téléphone technicien"]  = st.text_input("Numéro de téléphone")
    info_base["Chargé de projet"]  = st.text_input("Chargé de projet")

st.write("Résumé des informations")
st.json(info_base,expanded=False)
st.divider()
st.header("Démarrage de la mise en service")
validation_preconisation = st.selectbox("Avez-vous pris connaissance des préconisations constructeur ?", ("Oui", "Non"),index=1)
if validation_preconisation == "Oui":
    st.info("Veuillez vérifier tous les supports et fixations de la machine", icon="ℹ️")
elif validation_preconisation == "Non":
    st.warning("Veuillez prendre connaissance des préconisations constructeur avant la mise en service", icon="⚠️")
st.divider()
st.header("Test de pression")
st.subheader("test de pression ps +10%")
validation_test_pression = st.selectbox("Avez-vous testé le circuit à une pression ps+10% ?", ("Oui", "Non"),index=1)
if validation_test_pression == "Oui":
    st.info("Renseigner la durée de mise sous pression",icon="ℹ️")
elif validation_test_pression == "Non":
    st.warning("Veuillez tester le circuit à une pression ps+10\% d'une durée de 48h",icon="⚠️")
    
df_pression = pd.DataFrame({"Circuit":["Bp","Mp","Hp"],"Pression (Bar)":[0,0,0],"Durée(h)":[0,0,0]}).set_index("Circuit")
df_pression = st.data_editor(df_pression)
st.info("Si existence d'une soupape sur le circuit, Pt = p(soupape) - 10% p(soupape) = 0.8 p(soupape)",icon="⚠️")
fuite = st.selectbox("Avez-vous constaté une fuite sur le circuit frigorifique ?", ("Oui", "Non"))
st.divider()
st.header("Partie électrique")
validation_EPI = st.selectbox("Avez-vous vos EPI?",("Oui","Non"),index=1)
validation_schema = ""
if validation_EPI == "Oui":
    validation_schema = st.selectbox("Avez-vous le schéma électrique et le PID de l'installation ?", ("Oui", "Non"),index=1)
    if validation_schema == "Non":
        st.warning("Veuillez procurer le schéma électrique + PID de la machine")
elif validation_EPI == "Non":
    st.error("Veuillez vous équiper de vos EPI avant toute mise en service électrique",icon="🚨")

#######################################
if validation_schema == "Oui":
    st.subheader("Compresseurs")
    st.write("La machine contient combien de CP ?")
    nb_compresseur = st.text_input("Nombres: ")
    
    try:
        dict_compresseurs = {
            f"CP{n}": ["","","","","","","",""] for n in range(1, int(nb_compresseur) + 1)
        }
        df_compresseur = pd.DataFrame(
        {
            "Information":["Fabriquement","Modèle","N° de série","Tension (V)","Fréquence (Hz)","couplage(Δ) ou Y", "Intensité plaqué (A)","Intensité règle en GV (A)"],
            **dict_compresseurs
        }).set_index("Information")
    
        df_compresseur = st.data_editor(df_compresseur)
    except:
        st.info("Définir le nombre de compresseurs")
    
    st.info("Veuillez vérifier le serrage sur les circuits de puissance et de commande",icon="⚠️")

    ###################################################################
    st.subheader("Kriwan")
    validation_kriwon = st.selectbox("Avez-vous testé la sonde de Kriwan de tous les compresseurs ?", ("Oui", "Non"),index=1)
    st.subheader("Essai pressorstats Bp/Hp de sécurité")
    validation_pressorstat = st.selectbox("Avez-vous testé les pressorstats Bp/Hp de sécurité de chaque CP ?", ("Oui", "Non"),index=1)
    st.subheader("Essai de contrôleur de niveau d'huile")
    validation_huile = st.selectbox("Avez-vous testé le contrôleur de niveau d'huile ?",("Oui", "Non"),index=1)
    st.divider()
    st.header("Evacuation de vide")
    validation_resistance = st.selectbox("Resistance de carter des compresseurs en marche pendant le tirage au vide ?",("Oui", "Non"))
    temp_ext = st.slider("Veuillez renseigner la température extérieur en °C",min_value=-20,max_value=50,value=20)
    pression_vide = st.number_input("Veuillez renseigner la pression de vide affichée au vacuometre em mbar")
    validation_hygro = st.selectbox("Le voyant hygroscopique est de couleur verte (bouteille liquide)",("Oui", "Non"),index=1)
    st.divider()
    st.header("Niveau d'huile")
    st.info("Veuillez vérifier que l'huile correspond au type d'huile mentionné sur l'étiquette du chassis")
    validation_qt_huile = st.selectbox("Quantité d'huile remplie est inférieure ou égale à la contenance de réservoir d'huile mentionnée sur la plaque signalétique",("Oui", "Non"),index=1)
    st.divider()
    st.header("Mise sous pression du système")
    pression_vapeur = st.number_input("Quelle est la pression (bar) de vapeur de fluide frigogène rempli dans toutes les sections de l'installation ?")
    st.divider()
    st.header("Rapport PDF")
    # Génére un rapport PDF regroupant toutes les informations rentrées par l'utilisateur
    if st.button("Générer le rapport PDF"):
        html = f"""
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Rapport PDF</title>
                </head>
                <body>
                    <h1>Informations de base</h1>
                    <ul>
                        <li>N° de la machine: {info_base.get("N° de la machine", "")}</li>
                        <li>Adresse de l'installation: {info_base.get("Adresse de l'installation", "")}</li>
                        <li>Utilisateur: {info_base.get("Utilisateur", "")}</li>
                        <li>Date de mise en service: {info_base.get("Date de mise en service", "")}</li>
                        <li>FF: {info_base.get("FF", "")}</li>
                        <li>Huile: {info_base.get("Huile", "")}</li>
                    </ul>
                    <h1>Informations sur l'installateur</h1>
                    <ul>
                        <li>Nom du Technicien: {info_base.get("Nom du Technicien", "")}</li>
                        <li>N° de téléphone technicien: {info_base.get("N° de téléphone technicien", "")}</li>
                        <li>Chargé de projet: {info_base.get("Chargé de projet", "")}</li>
                    </ul>
                    <h1>Démarrage de la mise en service</h1>
                    <ul>
                        <li>Avez-vous pris connaissance des préconisations constructeur ?: {validation_preconisation}</li>
                    </ul>
                    <h1>Test de pression</h1>
                    <ul>
                        <li>Avez-vous testé le circuit à une pression p5+10% ?: {validation_test_pression}</li>
                    </ul>
                    <h1>Pression</h1>
                    {df_pression.to_html()}
                    <ul>
                        <li>Avez-vous constaté une fuite sur le circuit frigorifique ?: {fuite}</li>
                    </ul>
                    <h1>Partie électrique</h1>
                    <ul>
                        <li>Avez-vous vos EPI?: {validation_EPI}</li>
                        <li>Avez-vous le schéma électrique et le PIB de l'installation ?: {validation_schema}</li>
                    </ul>
                    <h2>Compresseurs</h2>
                    {df_compresseur.to_html()}
                    <ul>
                        <li>Avez-vous testé la sonde de Kriwan de tous les compresseurs ?: {validation_kriwon}</li>
                        <li>Avez-vous testé les pressostats Bp/Hp de sécurité de chaque CP ?: {validation_pressorstat}</li>
                        <li>Avez-vous testé le contrôleur de niveau d'huile ?: {validation_huile}</li>
                    </ul>
                    <h1>Evacuation de vide</h1>
                    <ul>
                        <li>Resistance de carter compresseurs en marche pendant le triage au vide ?: {validation_resistance}</li>
                        <li>Température extérieur en °C: {temp_ext}</li>
                        <li>Pression de vide affichée au vacametre em mbar: {pression_vide}</li>
                        <li>Le voyant hygroscopique est de couleur verte (bouteille liquide) ?: {validation_hygro}</li>
                    </ul>
                    <h1>Niveau d'huile</h1>
                    <ul>
                        <li>Quantité d'huile remplie est inférieure ou égale à la contenance de réservoir d'huile mentionnée sur la plaque signalétique ?: {validation_qt_huile}</li>
                    </ul>
                    <h1>Mise sous pression du système</h1>
                    <ul>
                        <li>Pression (bar) de vapeur de fluide frigogène rempli dans toutes les sections de l'installation ?: {pression_vapeur}</li>
                    </ul>
                </body>
            </html>
        """

        nom_fichier = f'Rapport_mise_en_service_{datetime.today().day}{datetime.today().month}{datetime.today().year}.pdf'

        pdfkit.from_string(html, nom_fichier)

        with open(nom_fichier,"rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button("Télécharger le rapport PDF", PDFbyte, nom_fichier, mime="application/octet-stream")