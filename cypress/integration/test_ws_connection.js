describe('Test Login', function() {
  it("User can login through UI", function() {
    cy.login();
    cy.visit("/examples/websockets")
    cy.get("#ping").click();
    cy.get('.pong').should('have.length', 1);
  });
});
