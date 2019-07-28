describe('Test Login', function() {
  it("User can logout after having logged in.", function() {
    cy.login();
    cy.visit("/");
    cy.getCookies()
      .should('have.length', 2);
    cy.get("#logout").click();
    cy.getCookies()
    .should('have.length', 0)
  });
});
