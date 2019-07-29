describe('Test websockets', function() {
  it("User sees PONG message from websocket PING message", function() {
    cy.login();
    cy.visit("/examples/websockets")
    cy.get("#ping").click();
    cy.wait(500);
    cy.get('.pong').should('have.length', 1);
  });
});
