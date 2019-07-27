describe('Test Login', function() {
  it("User can login through UI", function() {
    cy.login();
    cy.visit("/examples/websockets")
    cy.get("#ping").click();
    cy.get("#ping").click();
    cy.get("#ping").click();
    cy.wait(200);
    cy.get('.pong').should('have.length', 3)
  });
});
