describe('Page Résultats', () => {

  context('Utilisateur authentifié', () => {

    beforeEach(() => {
      cy.clearLocalStorage();
      cy.visit("http://localhost:5173");
      cy.wait(500);
      cy.loginAsAdmin();
      cy.visit("/results");
    });

    it('affiche le loader au chargement', () => {
      cy.contains('Chargement...').should('exist');
    });

    it('affiche la section des matchs', () => {
      cy.contains('Matchs les plus récents').should('be.visible');

      cy.get('body').then(($body) => {
        if ($body.text().includes('Aucun résultat disponible')) {
          cy.contains('Aucun résultat disponible').should('be.visible');
        } else {
          cy.contains('Match du').should('exist');
          cy.contains('Score:').should('exist');
        }
      });
    });

    it('affiche la section classement', () => {
      cy.contains('Classement des équipes du tournois').should('be.visible');

      cy.get('body').then(($body) => {
        if ($body.text().includes('Aucun classement disponible')) {
          cy.contains('Aucun classement disponible').should('be.visible');
        } else {
          cy.contains('Position :').should('exist');
          cy.contains('Points:').should('exist');
        }
      });
    });

  });

});
