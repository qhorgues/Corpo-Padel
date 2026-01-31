describe('Planning – tests E2E avec backend réel', () => {
  let createdEventTime

  before(() => {
    const now = new Date()
    createdEventTime = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`
  })

  beforeEach(() => {
    cy.clearLocalStorage()
    cy.visit('http://localhost:5173')
    cy.wait(500)
    cy.loginAsAdmin()
    cy.visit('/planning')
  })

  it('affiche le titre et la description', () => {
    cy.contains('Planning').should('be.visible')
    cy.contains('Calendrier de la saison').should('be.visible')
  })

  it('affiche le mois et l’année courants', () => {
    const monthNames = [
      'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
      'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]
    const now = new Date()
    const expected = `${monthNames[now.getMonth()]} ${now.getFullYear()}`
    cy.contains(expected).should('be.visible')
  })

  it('affiche la grille du calendrier', () => {
    ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'].forEach(day => {
      cy.contains(day).should('exist')
    })
  })

  it('permet de naviguer entre les mois', () => {
    cy.contains('Suivant →').click()
    cy.contains('← Précédent').click()
    cy.contains('Planning').should('be.visible')
  })

  it('le filtre "Voir uniquement mes événements" est coché par défaut', () => {
    cy.contains('Voir uniquement mes événements')
      .parent()
      .find('input[type="checkbox"]')
      .should('be.checked')
  })

  it('permet d’activer/désactiver le filtre', () => {
    const checkbox = cy.contains('Voir uniquement mes événements')
      .parent()
      .find('input[type="checkbox"]')
    checkbox.uncheck().should('not.be.checked')
    checkbox.check().should('be.checked')
  })

  it('ouvre une modale en cliquant sur un jour avec événement', () => {
    cy.contains('Voir uniquement mes événements')
      .parent()
      .find('input[type="checkbox"]')
      .uncheck()

    cy.get('button')
      .filter(':has(div.w-2.h-2)')
      .first()
      .then($btn => cy.wrap($btn).click())
    cy.contains('Événements du').should('be.visible')
  })

  it('ferme la modale des événements', () => {
    cy.contains('Voir uniquement mes événements')
      .parent()
      .find('input[type="checkbox"]')
      .uncheck()

    cy.get('button')
      .filter(':has(div.w-2.h-2)')
      .first()
      .click()
    cy.contains('Fermer').click()
    cy.contains('Événements du').should('not.exist')
  })

  it('n’ouvre rien en cliquant sur un jour sans événement', () => {
    cy.get('button')
      .filter(':not(:has(div.w-2.h-2))')
      .first()
      .click()
    cy.contains('Événements du').should('not.exist')
  })

  it('crée, modifie et supprime un événement', () => {
    cy.contains('Voir uniquement mes événements')
      .parent()
      .find('input[type="checkbox"]')
      .uncheck()

    cy.contains('Ajouter un événement').click()

    const today = new Date().toISOString().split('T')[0]
    cy.get('input[type="date"]').clear().type(today)
    cy.get('input[type="time"]').clear().type(createdEventTime)

    // Nombre de matchs et piste
    cy.get('select').contains('1 match').parent().select('1')
    cy.get('input[type="number"]').clear().type('1')

    // Équipes
    cy.get('select').eq(1).find('option').eq(1).then(opt => cy.get('select').eq(1).select(opt.val()))
    cy.get('select').eq(2).find('option').eq(2).then(opt => cy.get('select').eq(2).select(opt.val()))

    cy.get('div[role="dialog"]')
      .contains(/^Ajouter$/)
      .should('be.visible')
      .and('not.be.disabled')
      .click({ force: true })
    cy.wait(500)

    const dayOfMonth = today.split('-')[2]
    cy.get('button').contains(new RegExp(`^${dayOfMonth}$`)).click()

    cy.contains(createdEventTime)
    .closest('div')
    .parent()
    .within(() => cy.get('button').contains('Modifier').click())

    const newTime = '23:00'
    cy.get('div[role="dialog"]').get('input[type="time"]').clear().type(newTime)
    cy.get('div[role="dialog"]')
      .contains(/^Enregistrer$/)
      .should('be.visible')
      .and('not.be.disabled')
      .click({ force: true })

    cy.get('button').contains(new RegExp(`^${today.split('-')[2]}$`)).click()

    cy.contains(newTime)
    .closest('div')
    .parent()
    .within(() => cy.get('button').contains('Supprimer').click())
    cy.get('div[role="dialog"]')
      .contains(/^Supprimer$/)
      .should('be.visible')
      .and('not.be.disabled')
      .click({ force: true })

    cy.contains(newTime).should('not.exist')
  })
})
