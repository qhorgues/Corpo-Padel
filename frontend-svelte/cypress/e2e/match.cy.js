// cypress/e2e/matches.cy.ts
describe("Gestion des matchs", () => {
  const today = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
  const matchTime = "16:00"; // heure fixe pour le test

  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit("http://localhost:5173");
    cy.wait(500);
    cy.loginAsAdmin();
    cy.visit("/matches");
  });

  it("ajoute un match", () => {
    cy.contains("➕ Ajouter un match").click();

    // Remplir le formulaire
    cy.get('input[type="date"]').clear().type(today);
    cy.get('input[type="time"]').clear().type(matchTime);
    cy.get('input[type="number"]').clear().type("1"); // Piste 1

    // Sélectionner les équipes
    cy.get("div[role='dialog']")
      .find("select")
      .eq(0)
      .select(1, { force: true });
    cy.get("div[role='dialog']")
      .find("select")
      .eq(1)
      .select(2, { force: true });

    // Valider
    cy.get("div[role='dialog']")
      .find("button.bg-blue-600")
      .click({ force: true });

    cy.wait(500);

    // Vérifier que le match apparaît
    cy.contains(`Piste 1`).should("exist");
  });

  it("modifie un match existant", () => {
    // Sélectionner le match créé aujourd'hui
    cy.contains(`Piste 1`)
      .closest("div.bg-white")
      .within(() => {
        cy.contains("✏️ Modifier").click();
      });

    // Modifier le court_number et le statut
    cy.get("div[role='dialog']")
      .find('input[type="number"]')
      .clear()
      .type("2");

    cy.get("div[role='dialog']")
      .find("button.bg-blue-600")
      .click({ force: true });

    cy.wait(500);

    cy.contains("Piste 2").should("exist");
  });

  it("supprime un match existant", () => {
    cy.contains("Piste 2")
      .closest("div.bg-white")
      .within(() => {
        cy.contains("🗑️ Supprimer").click();
      });

    // Confirmer la suppression
    cy.get("div[role='dialog']")
      .contains("Supprimer")
      .click({ force: true });

    cy.wait(500);

    // Vérifier que le match a disparu
    cy.contains("Piste 2").should("not.exist");
  });
});
