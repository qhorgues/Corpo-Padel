describe('Admin – Players / Teams / Pools (E2E)', () => {
    describe('Admin connecté', () => {

    describe('Gestion des joueurs', () => {

      beforeEach(() => {
        cy.clearLocalStorage();
        cy.visit("http://localhost:5173");
        cy.wait(500);
        cy.loginAsAdmin();
        cy.visit("/admin");
      });

      it('affiche la liste des joueurs', () => {
        cy.contains('Liste des joueurs').should('be.visible');
        cy.contains('Chargement...').should('not.exist');
      });

      it('ouvre la modale de création', () => {
        cy.contains('Créer utilisateur').click();
        cy.contains('Créer un utilisateur').should('be.visible');
      });

      it('bloque la création si formulaire invalide', () => {
        cy.contains('Créer utilisateur').click();
        cy.get('.fixed.inset-0.z-50')
          .should('be.visible')
          .within(() => {
            cy.contains('Créer').click();
          });
        cy.contains('Créer utilisateur').should('exist');
      });

      it('crée un joueur', () => {
        const license = `L${Date.now().toString().slice(-6)}`;
        const email = `player${Date.now()}@test.com`;

        cy.contains('Créer utilisateur').click();

        cy.get('input').eq(0).type('Test');
        cy.get('input').eq(1).type('Player');
        cy.get('select').first().select(1);
        cy.get('input[placeholder="L123456"]').type(license);
        cy.get('input[type="email"]').type(email);

        cy.get('.fixed.inset-0.z-50')
          .should('be.visible')
          .within(() => {
            cy.contains('Créer').click();
          });
        cy.contains('Test').should('exist');
      });

    });

    describe('Gestion des équipes & poules', () => {

      beforeEach(() => {
        cy.clearLocalStorage();
        cy.visit("http://localhost:5173");
        cy.wait(500);
        cy.loginAsAdmin();
        cy.visit("/admin/teams-pools");
      });

      it('affiche la page', () => {
          cy.contains('Gestion des équipes et poules').should('be.visible');
        });

        it('crée une poule', () => {
        const poolName = `Poule ${Date.now()}`;

        cy.contains('Poules').click();
        cy.contains('Ajouter une poule').click();

        cy.get('.fixed.inset-0.z-50').within(() => {
          cy.get('input[placeholder="Ex: Poule A"]').type(poolName);
          cy.contains('Ajouter').click();
        });

        cy.contains(poolName).should('exist');
      });

      it('refuse deux fois le même joueur', () => {
        cy.contains('Équipes').click();
        cy.contains('Ajouter une équipe').click();

        cy.get('.fixed.inset-0.z-50').within(() => {
          cy.get('select').eq(0).select(1);
          cy.get('select').eq(1).select(1);
          cy.get('select').eq(2).select(1);

          cy.on('window:alert', (msg) => {
            expect(msg).to.contain('Les deux joueurs doivent être différents');
          });

          cy.contains('Ajouter').click();
        });
      });


    });

  });

});
