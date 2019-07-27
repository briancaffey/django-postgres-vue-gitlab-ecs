describe('Test Login', function() {
  it('Finds the text of the homepage', function() {
    cy.visit("/");
    cy.get("#login").click();
    cy.get("#login-btn").click()
  });
});
