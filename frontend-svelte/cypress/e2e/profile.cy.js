// cypress/e2e/profile.cy.ts
describe("Page Profil Utilisateur (vrai serveur)", () => {

  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit("http://localhost:5173");
    cy.wait(500);
    cy.loginAsAdmin();
    cy.visit("/profile");
  });

  it("affiche le profil pour un utilisateur connecté", () => {
    cy.contains("Chargement...").should("not.exist");

    cy.contains("Profil utilisateur").should("exist");
    cy.get("img[alt='Photo de profil']").should("exist");

    cy.get("p").contains("Nom :").should("exist");
    cy.get("p").contains("Prénom :").should("exist");
    cy.get("p").contains("Email :").should("exist");
    cy.contains("Éditer les informations").should("exist");
  });

  it("affiche un message d'erreur si le profil ne se charge pas", () => {
    cy.clearLocalStorage();
    cy.visit("/profile");

    cy.contains("Connectez-vous pour accéder à votre planning, vos matchs et vos résultats").should("exist");
  });

  it("affiche le formulaire avec les données actuelles de l'utilisateur", () => {
    cy.visit("/profile/edit")
    cy.contains("Chargement...").should("not.exist");

    cy.contains("Éditer le profil").should("exist");

    cy.get("#first_name").should("have.value").and("not.be.empty");
    cy.get("#last_name").should("have.value").and("not.be.empty");
    cy.get("#birth_date").should("have.value").and("not.be.empty");
    cy.get("#email").should("have.value").and("not.be.empty");
    cy.get("#company").should("be.disabled");
    cy.get("#license_number").should("be.disabled");
    cy.get("#photo_url").should("have.value");
  });

  it("permet de modifier le prénom et le nom et de sauvegarder", () => {
    cy.wait(500)
    cy.visit("/profile/edit")
    cy.contains("Chargement...").should("not.exist");

    const newFirstName = "TestPrénom";
    const newLastName = "TestNom";

    cy.get("#first_name").clear().type(newFirstName);
    cy.get("#last_name").clear().type(newLastName);

    cy.get("button").contains("Sauvegarder").click();

    cy.on("window:alert", (text) => {
      expect(text).to.contains("Profil mis à jour avec succès");
    });

    cy.url().should("eq", "http://localhost:5173/profile");

    cy.contains(`Nom : ${newLastName}`).should("exist");
    cy.contains(`Prénom : ${newFirstName}`).should("exist");
  });

  it("bouton Annuler retourne sur la page profil sans sauvegarder", () => {
    cy.wait(500)
    cy.visit("/profile/edit")
    cy.contains("Chargement...").should("not.exist");

    const originalFirstName = cy.get("#first_name").invoke("val");
    
    cy.get("#first_name").invoke("val").then((originalFirstName) => {
      cy.get("button").contains("Annuler").click();
      cy.url().should("eq", "http://localhost:5173/profile");
      cy.contains(`Prénom : ${originalFirstName}`).should("exist");
    });
  });

  it("les champs non éditables restent désactivés", () => {
    cy.wait(500)
    cy.visit("/profile/edit")

    cy.get("#company").should("be.disabled");
    cy.get("#license_number").should("be.disabled");
  });

});
