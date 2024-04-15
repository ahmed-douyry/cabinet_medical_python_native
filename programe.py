from email.message import EmailMessage
from email.mime import message
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from fpdf import FPDF

class FormulaireInscription(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Formulaire d'inscription")
        
        # Créer les widgets du formulaire d'inscription
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        # Image à gauche
        background_image = tk.PhotoImage(file="PHOTO.png")
        self.image_label = tk.Label(self.canvas, image=background_image)
        self.image_label.place(relwidth=0.3, relheight=1)
        
        # Titre et sous-titre à droite
        self.title_label = tk.Label(self.canvas, text="Bienvenue", font=("Arial", 20), fg="blue")
        self.title_label.place(relx=0.72, rely=0.1, anchor="center")
        self.subtitle_label = tk.Label(self.canvas, text="Créez votre compte", font=("Arial", 16))
        self.subtitle_label.place(relx=0.72, rely=0.2, anchor="center")
        
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect("cabinet_ophtalmologique.db")
        self.c = self.conn.cursor()

        # Créer la table si elle n'existe pas déjà
        self.c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs
                        (id INTEGER PRIMARY KEY,
                        genre TEXT,
                        nom TEXT,
                        prenom TEXT,  
                        cin TEXT,
                        telephone TEXT,
                        email TEXT,
                        mot_de_passe TEXT,
                        rendez_vous_jour TEXT,
                        rendez_vous_heure TEXT)''')
        self.conn.commit()

        # Créer la table si elle n'existe pas déjà
        self.c.execute('''CREATE TABLE IF NOT EXISTS messages
                        (id INTEGER PRIMARY KEY,
                        email text,
                        message text )''')
        self.conn.commit()

        

        

        # Créer les widgets du formulaire d'inscription
        self.create_widgets()

    def create_widgets(self):
        # Genre (checkbox)
        self.genre_frame = tk.Frame(self.canvas)
        self.genre_frame.place(relx=0.8, rely=0.3, anchor="e")
        self.genre_label = tk.Label(self.genre_frame, text="Genre:", font=("Arial", 12))
        self.genre_label.pack(side="left")
        self.genre_var = tk.StringVar(value="Féminin")
        self.genre_male = tk.Radiobutton(self.genre_frame, text="Masculin", variable=self.genre_var, value="Masculin")
        self.genre_female = tk.Radiobutton(self.genre_frame, text="Féminin", variable=self.genre_var, value="Féminin")
        self.genre_male.pack(side="left", padx=5)
        self.genre_female.pack(side="left", padx=5)

        # Nom
        self.name_frame = tk.Frame(self.canvas)
        self.name_frame.place(relx=0.8, rely=0.4, anchor="e")
        self.name_label = tk.Label(self.name_frame, text="Nom:", font=("Arial", 12))
        self.name_label.pack(side="left", padx=5)
        self.name_entry = tk.Entry(self.name_frame, font=("Arial", 12))
        self.name_entry.pack(side="left", padx=5)

        # Prénom
        self.prenom_frame = tk.Frame(self.canvas)
        self.prenom_frame.place(relx=0.8, rely=0.45, anchor="e")
        self.prenom_label = tk.Label(self.prenom_frame, text="Prénom:", font=("Arial", 12))
        self.prenom_label.pack(side="left", padx=5)
        self.prenom_entry = tk.Entry(self.prenom_frame, font=("Arial", 12))
        self.prenom_entry.pack(side="left", padx=5)

        # CIN
        self.cin_frame = tk.Frame(self.canvas)
        self.cin_frame.place(relx=0.8, rely=0.5, anchor="e")
        self.cin_label = tk.Label(self.cin_frame, text="CIN:", font=("Arial", 12))
        self.cin_label.pack(side="left", padx=5)
        self.cin_entry = tk.Entry(self.cin_frame, font=("Arial", 12))
        self.cin_entry.pack(side="left", padx=5)

        # Téléphone
        self.tel_frame = tk.Frame(self.canvas)
        self.tel_frame.place(relx=0.8, rely=0.55, anchor="e")
        self.tel_label = tk.Label(self.tel_frame, text="Téléphone:", font=("Arial", 12))
        self.tel_label.pack(side="left", padx=5)
        self.tel_entry = tk.Entry(self.tel_frame, font=("Arial", 12))
        self.tel_entry.pack(side="left", padx=5) 

        # Adresse email
        self.email_frame = tk.Frame(self.canvas)
        self.email_frame.place(relx=0.8, rely=0.6, anchor="e")
        self.email_label = tk.Label(self.email_frame, text="Adresse Email:", font=("Arial", 12))
        self.email_label.pack(side="left", padx=5)
        self.email_entry = tk.Entry(self.email_frame, font=("Arial", 12))
        self.email_entry.pack(side="left", padx=5)

        # Mot de passe
        self.password_frame = tk.Frame(self.canvas)
        self.password_frame.place(relx=0.8, rely=0.65, anchor="e")
        self.password_label = tk.Label(self.password_frame, text="Mot de Passe:", font=("Arial", 12))
        self.password_label.pack(side="left", padx=5)
        self.password_entry = tk.Entry(self.password_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(side="left", padx=5)

        # Confirmation du mot de passe
        self.confirm_password_frame = tk.Frame(self.canvas)
        self.confirm_password_frame.place(relx=0.8, rely=0.7, anchor="e")
        self.confirm_password_label = tk.Label(self.confirm_password_frame, text="Confirmer Mot de Passe:", font=("Arial", 12))
        self.confirm_password_label.pack(side="left", padx=5)
        self.confirm_password_entry = tk.Entry(self.confirm_password_frame, show="*", font=("Arial", 12))
        self.confirm_password_entry.pack(side="left", padx=5)

        # Sélectionner le jour du rendez-vous
        self.jour_frame = tk.Frame(self.canvas)
        self.jour_frame.place(relx=0.8, rely=0.75, anchor="e")
        self.jour_label = tk.Label(self.jour_frame, text="Jour du rendez-vous:", font=("Arial", 12))
        self.jour_label.pack(side="left", padx=5)
        self.jour_entry = tk.Entry(self.jour_frame, font=("Arial", 12))
        self.jour_entry.pack(side="left", padx=5)

        # Heure du rendez-vous
        self.heure_frame = tk.Frame(self.canvas)
        self.heure_frame.place(relx=0.8, rely=0.8, anchor="e")
        self.heure_label = tk.Label(self.heure_frame, text="Heure du rendez-vous:", font=("Arial", 12))
        self.heure_label.pack(side="left", padx=5)
        self.heure_entry = tk.Entry(self.heure_frame, font=("Arial", 12))
        self.heure_entry.pack(side="left", padx=5)

        # Bouton "S'inscrire"
        self.inscrire_button = tk.Button(self.canvas, text="S'inscrire", font=("Arial", 14), bg="blue", fg="white", command=self.s_inscrire)
        self.inscrire_button.place(relx=0.7, rely=0.9, anchor="center")

        

    def afficher_liste_patients(self):
        self.c.execute("SELECT * FROM utilisateurs")
        patients = self.c.fetchall()
        if patients:
            ListePatients(self, patients)
        else:
            messagebox.showinfo("Liste des patients", "Aucun patient enregistré.")

    def s_inscrire(self):
        # Récupérer les valeurs des champs du formulaire
        genre = self.genre_var.get()
        nom = self.name_entry.get()
        prenom = self.prenom_entry.get()
        cin = self.cin_entry.get()
        telephone = self.tel_entry.get()
        email = self.email_entry.get()
        mot_de_passe = self.password_entry.get()
        confirmation_mot_de_passe = self.confirm_password_entry.get()
        rendez_vous_jour = self.jour_entry.get()
        rendez_vous_heure = self.heure_entry.get()

        # Vérifier si les champs obligatoires sont remplis
        if not (genre and nom and prenom and cin and telephone and email and mot_de_passe and rendez_vous_jour and rendez_vous_heure):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        # Vérifier si les mots de passe correspondent
        if mot_de_passe != confirmation_mot_de_passe:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        # Vérifier si l'utilisateur n'est pas déjà inscrit avec le même email
        self.c.execute("SELECT * FROM utilisateurs WHERE email=?", (email,))
        if self.c.fetchone():
            messagebox.showerror("Erreur", "Cet email est déjà utilisé.")
            return

        # Insérer les données dans la base de données
        try:
            self.c.execute('''INSERT INTO utilisateurs (genre, nom, prenom, cin, telephone, email, mot_de_passe, rendez_vous_jour, rendez_vous_heure)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (genre, nom, prenom, cin, telephone, email, mot_de_passe, rendez_vous_jour, rendez_vous_heure))
            self.conn.commit()
            messagebox.showinfo("Inscription réussie", "Votre inscription a été enregistrée avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'inscription : {e}")
            return

        # Fermer la fenêtre de formulaire
        self.destroy()

class ListePatients(tk.Toplevel):
    def __init__(self, parent, patients):
        super().__init__(parent)
        self.title("Liste des patients")
        
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Genre", "Nom", "Prénom", "CIN", "Téléphone", "Email", "Jour Rendez-vous", "Heure Rendez-vous")

        self.tree.heading("#0", text="ID")
        self.tree.column("#0", minwidth=0, width=50, stretch=tk.NO)
        self.tree.heading("Genre", text="Genre")
        self.tree.column("Genre", minwidth=0, width=100, stretch=tk.NO)
        self.tree.heading("Nom", text="Nom")
        self.tree.column("Nom", minwidth=0, width=100, stretch=tk.NO)
        self.tree.heading("Prénom", text="Prénom")
        self.tree.column("Prénom", minwidth=100, stretch=tk.NO)
        self.tree.heading("CIN", text="CIN")
        self.tree.column("CIN", minwidth=0, width=100, stretch=tk.NO)
        self.tree.heading("Téléphone", text="Téléphone")
        self.tree.column("Téléphone", minwidth=0, width=100, stretch=tk.NO)
        self.tree.heading("Email", text="Email")
        self.tree.column("Email", minwidth=0, width=150, stretch=tk.NO)
        self.tree.heading("Jour Rendez-vous", text="Jour Rendez-vous")
        self.tree.column("Jour Rendez-vous", minwidth=0, width=150, stretch=tk.NO)
        self.tree.heading("Heure Rendez-vous", text="Heure Rendez-vous")
        self.tree.column("Heure Rendez-vous", minwidth=0, width=150, stretch=tk.NO)

        for patient in patients:
            self.tree.insert("", tk.END, text=str(patient[0]), values=(patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[8], patient[9]))

        self.tree.pack(expand=True, fill=tk.BOTH)
        
        
        

        # Button pour enregistrer comme pdf
        self.pdf_button = ttk.Button(self, text="Enregistrer comme PDF", command=self.save_as_pdf)
        self.pdf_button.pack(side=tk.LEFT, padx=10, pady=10)

    def print_patient_info(self):
        # Retrouver l element selectione
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un patient.")
            return
        
        values = self.tree.item(item, "values")
        # Print the patient information
        print("Patient Information:")
        print("Genre:", values[0])
        print("Nom:", values[1])
        print("Prénom:", values[2])
        print("CIN:", values[3])
        print("Téléphone:", values[4])
        print("Email:", values[5])
        print("Jour Rendez-vous:", values[6])
        print("Heure Rendez-vous:", values[7])

    def save_as_pdf(self):
    # Retrieve the selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un patient.")
            return

        # Retrieve the values associated with the selected item
        values = self.tree.item(selected_item, "values")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Patient Information", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Genre: {values[0]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Nom: {values[1]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Prénom: {values[2]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"CIN: {values[3]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Téléphone: {values[4]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Email: {values[5]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Jour Rendez-vous: {values[6]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Heure Rendez-vous: {values[7]}", ln=True, align="L")

        pdf_file = f"{values[1]} {values[2]}.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Information", f"Les informations du patient ont été enregistrées sous {pdf_file}.")
def afficher_liste_patients():
    conn = sqlite3.connect("cabinet_ophtalmologique.db")
    c = conn.cursor()
    c.execute("SELECT * FROM utilisateurs")
    patients = c.fetchall()
    if patients:
        ListePatients(root, patients)
    else:
        messagebox.showinfo("Liste des patients", "Aucun patient enregistré.")

# Fonction pour ouvrir une nouvelle fenêtre pour l'inscription
def ouvrir_page_inscription():
    formulaire_inscription = FormulaireInscription(root)

class PageContact(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Contactez-nous")

        
        # Titre "Contacter-nous ici !" centré au milieu de la page
        self.title_label = tk.Label(self, text="CONTACTER-NOUS ICI !", font=("Arial", 20))
        self.title_label.pack(pady=20)
        # Sous-titre "Nous sommes à votre écoute"
        self.subtitle_label = tk.Label(self, text=" NOUS SOMMES À VOTRE ÉCOUTE!", font=("Arial", 12))
        self.subtitle_label.pack(pady=10)
        # Champ pour l'adresse email
        self.email_label = tk.Label(self, text="Votre email:", font=("Arial", 12))
        self.email_label.pack()
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        # Champ pour le message
        self.message_label = tk.Label(self, text="Votre message:", font=("Arial", 12))
        self.message_label.pack()
        self.message_text = tk.Text(self, height=10, width=50)
        self.message_text.pack(pady=5)
        self.message_text.insert(tk.END, "Veuillez remplir ce champ si vous avez des commentaires, des questions ou des idées.")
        # Bouton "Envoyer"
        self.send_button = tk.Button(self, text="Envoyer", bg="#90EE90",font=("Arial", 12), command=self.envoyer_message)
        self.send_button.pack(pady=10)
        # self.button_comments = tk.Button(self, text="Liste des patients",bg="#90EE90", font=("Arial", 12), command=lambda: afficher_liste_patients())
        # self.button_comments.pack(pady=15)
        # self.send_button = tk.Button(self, text="Acceuil", bg="#ADD8E6",font=("Arial", 12), command=self.envoyer_message)
        # self.send_button.pack(pady=10)
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect("cabinet_ophtalmologique.db")
        self.c = self.conn.cursor()

        
       
      
        
    def envoyer_message(self):
        # Récupérer l'email et le message
        email = self.email_entry.get()
        message = self.message_text.get("1.0", tk.END)

        
        # Vérifier si les champs sont remplis
        if not email or not message.strip():
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
        # Insérer le message dans la base de données
        try:
            self.c.execute('''INSERT INTO messages (email, message) VALUES (?, ?)''', (email, message))
            self.conn.commit()
            messagebox.showinfo("Message envoyé", "Votre message a été envoyé avec succès.")
            self.destroy()  # Fermer la fenêtre après l'envoi du message
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'envoi du message : {e}")

class FenetreVisite(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nouvelle Visite Médicale")
        
        # Configuration du fond
        self.configure(bg="light green", bd=0, relief=tk.FLAT)
        
        # Champ pour le nom
        self.nom_label = tk.Label(self, text="Nom:", bg="light green", font=("Arial", 20))
        self.nom_label.grid(row=0, column=0, padx=30, pady=20)
        self.nom_entry = tk.Entry(self)
        self.nom_entry.grid(row=0, column=1, padx=30, pady=20)

        # Champ pour le prénom
        self.prenom_label = tk.Label(self, text="Prénom:", bg="light green",  font=("Arial", 20))
        self.prenom_label.grid(row=1, column=0, padx=30, pady=20)
        self.prenom_entry = tk.Entry(self)
        self.prenom_entry.grid(row=1, column=1, padx=30, pady=20)

        # Champ pour la date de visite
        self.date_label = tk.Label(self, text="Date visite:", bg="light green", font=("Arial", 20))
        self.date_label.grid(row=2, column=0, padx=30, pady=20)
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=30, pady=20)
        
        # Champ pour l'heure de visite
        self.heure_label = tk.Label(self, text="Heure visite:", bg="light green", font=("Arial", 20))
        self.heure_label.grid(row=3, column=0, padx=30, pady=20)
        self.heure_entry = tk.Entry(self)
        self.heure_entry.grid(row=3, column=1, padx=30, pady=20)
        
        # Champ pour le code patient
        self.code_label = tk.Label(self, text="Code patient:", bg="light green", font=("Arial", 20))
        self.code_label.grid(row=4, column=0, padx=30, pady=20)
        self.code_entry = tk.Entry(self)
        self.code_entry.grid(row=4, column=1, padx=30, pady=20)
        
        # Champ pour le montant payé
        self.montant_label = tk.Label(self, text="Montant payé:", bg="light green", font=("Arial", 20))
        self.montant_label.grid(row=5, column=0, padx=30, pady=20)
        self.montant_entry = tk.Entry(self)
        self.montant_entry.grid(row=5, column=1, padx=30, pady=20)
        
        # Bouton pour enregistrer la visite
        self.enregistrer_button = tk.Button(self, text="Enregistrer", command=self.enregistrer_visite)
        self.enregistrer_button.grid(row=6, column=0, columnspan=2, padx=30, pady=20)

    def enregistrer_visite(self):
        # Récupérer les valeurs saisies
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        date_visite = self.date_entry.get()
        heure_visite = self.heure_entry.get()
        code_patient = self.code_entry.get()
        montant_paye = self.montant_entry.get()
        
        # Afficher les informations de la visite
        messagebox.showinfo("Informations de la visite",
                            f"Nom: {nom}\n"
                            f"Prénom: {prenom}\n"
                            f"Date visite: {date_visite}\n"
                            f"Heure visite: {heure_visite}\n"
                            f"Code patient: {code_patient}\n"
                            f"Montant payé: {montant_paye}")
def ouvrir_page_visite():
    fenetre_visite = FenetreVisite(root)
# Fonction pour ouvrir la fenêtre de visite médicale
def ouvrir_page_contact():
    page_contact = PageContact(root)
def ouvrir_page_services():
    # Créer une nouvelle fenêtre ou page pour les services
    services_window = tk.Toplevel(root)
    services_window.title("Nos Services")


    
    # Ajouter du texte pour décrire les services
    title_label = tk.Label(services_window, text="Nos Services:", font=("serif", 35, "bold"),fg="#26A69A")
    title_label.pack(pady=40)
    
    service1_label = tk.Label(services_window, text="1-Suivi et gestion des affections chroniques de l'œil :", font=("Arial", 20, "bold"),fg="#80CBC4" )
    service1_label.pack() 
    service1_description = tk.Label(services_window, text="Gestion à long terme des conditions oculaires chroniques telles que le diabète et l'hypertension artérielle, qui peuvent affecter la santé oculaire.",  font=("Arial", 13) )
    service1_description.pack()
    
    service2_label = tk.Label(services_window, text="2-Traitement des troubles de la paupière et du strabisme :", font=("Arial", 20, "bold"), fg="#80CBC4" )
    service2_label.pack()
    service2_description = tk.Label(services_window, text="Évaluation et traitement des problèmes de paupières, tels que les paupières tombantes (ptosis) ou les yeux qui louchent (strabisme).", font=("Arial", 13) )
    service2_description.pack()

    service2_label = tk.Label(services_window, text="3-Traitement des maladies rétiniennes :", font=("Arial", 20, "bold"), fg="#80CBC4" )
    service2_label.pack()
    service2_description = tk.Label(services_window, text="Diagnostic et traitement des affections de la rétine, telles que la dégénérescence maculaire liée à l'âge (DMLA), la rétinopathie diabétique, etc.", font=("Arial", 13) )
    service2_description.pack()

    service2_label = tk.Label(services_window, text="4-Correction de la vision au laser :", font=("Arial", 20, "bold"), fg="#80CBC4" )
    service2_label.pack()
    service2_description = tk.Label(services_window, text="Correction de la myopie, de l'hypermétropie et de l'astigmatisme à l'aide de techniques chirurgicales au laser telles que LASIK, PRK, etc.", font=("Arial", 13) )
    service2_description.pack()

    service2_label = tk.Label(services_window, text="5-Consultations régulières de la vue :", font=("Arial", 20, "bold"), fg="#80CBC4")
    service2_label.pack()
    service2_description = tk.Label(services_window, text=" la prescription de lunettes ou de lentilles de contact et évaluation de la santé oculaire telles que le glaucome.", font=("Arial", 13) )
    service2_description.pack()

   # Ajouter la fonctionnalité de notation par des degrés
    rating_frame = tk.Frame(services_window)
    rating_frame.pack(pady=10)
    rating_label = tk.Label(rating_frame, text="Noter le service:", font=("Arial", 24), anchor="center")
    rating_label.grid(row=0, column=0, padx=10)

    # Créer des boutons radio pour chaque degré de notation
    ratings = [("Mauvais", b"red"), ("Moyen", b"orange"), ("Bon", b"yellow"), ("Très bon", b"green"), ("Excellent", b"limegreen")]
    rating_var = tk.StringVar()
    for i, (rating_text, color) in enumerate(ratings):
        rating_button = tk.Radiobutton(rating_frame, text=rating_text, variable=rating_var, value=i)
        rating_button.grid(row=5, column=i+1, padx=0)
        rating_button.config(fg=color)

# Ajouter un bouton "Envoyer" pour envoyer l'avis
    send_button = tk.Button(services_window, text="Envoyer", font=("Arial", 14), bg="#C8E6C9")
    send_button.pack(pady=20)
# fenêtre principale
root = tk.Tk()
root.title("Cabinet Ophtalmologique")

# Définir la taille de la fenêtre
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()

# Définir la géométrie de la fenêtre pour qu'elle soit en plein écran
root.geometry(f"{largeur_ecran-4}x{hauteur_ecran-70}+2-30")

# Créer un canevas avec un arrière-plan représentant un cabinet ophtalmologique
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# Ajouter une image d'arrière-plan représentant un cabinet ophtalmologique
background_image = tk.PhotoImage(file="PHOTO.png")
background_label = tk.Label(canvas, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Barre de navigation
navbar_frame = tk.Frame(canvas, bg="turquoise")
navbar_frame.pack(side="top", fill="x")

# Logo des yeux à gauche
left_eye_label = tk.Label(navbar_frame, text="👁️Cabinet Ophtalmologique        ", font=("Arial", 40), bg="turquoise")
left_eye_label.pack(side="left", padx=50)

# Liens de navigation

# Créer un lien pour accéder aux services
services_link = tk.Label(navbar_frame, text="Acceuil", font=("Arial", 12), bg="turquoise", cursor="hand2")
services_link.pack(side="left", padx=10)
services_link.bind("<Button-1> ")

services_link = tk.Label(navbar_frame, text="Services", font=("Arial", 12), bg="turquoise", cursor="hand2")
services_link.pack(side="left", padx=10)
services_link.bind("<Button-1>", lambda event: ouvrir_page_services())

services_link = tk.Label(navbar_frame, text="Contact", font=("Arial", 12), bg="turquoise", cursor="hand2")
services_link.pack(side="left", padx=10)
services_link.bind("<Button-1>", lambda event: ouvrir_page_contact())

services_link = tk.Label(navbar_frame, text="Visite", font=("Arial", 12), bg="turquoise", cursor="hand2")
services_link.pack(side="left", padx=10)
services_link.bind("<Button-1>", lambda event: ouvrir_page_visite())

# Titre centré
title_label = tk.Label(root, text="Au service de votre santé", font=("Arial", 20))
title_label.pack(pady=20)

# Citation sur l'ophtalmologie
quote_label = tk.Label(root, text="Votre vision est notre priorité.", font=("Arial", 12))
quote_label.pack(pady=10)

# Bouton "Prenez votre rendez-vous"
button = tk.Button(root, text="Prenez votre rendez-vous", font=("Arial", 14), bg="turquoise", command=ouvrir_page_inscription)
button.pack(pady=20)

# Bouton "Liste des patients"
button_liste_patients = tk.Button(root, text="Liste des patients", font=("Arial", 14), bg="turquoise", command=lambda: afficher_liste_patients())
button_liste_patients.pack(pady=20)

root.mainloop()


