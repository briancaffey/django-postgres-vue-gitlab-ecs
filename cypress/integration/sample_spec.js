describe('Visit homepage and verify title', function() {
  it('Finds the text of the homepage', function() {
    cy.visit(Cypress.config('baseUrl'));
  });
  it('Finds the text of the homepage', function() {
    cy.visit("/");
  })
});
