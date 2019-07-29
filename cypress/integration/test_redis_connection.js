describe('Test redis connection', function() {
  it("can set value to redis key", function() {
    cy.login();
    cy.visit("/examples/redis");
    cy.get("#clear").click();
    cy.get('#val').should('be.empty');

    cy.get("#input").type(8);
    cy.get("#set").click();
    cy.get(".redis-debug").find("#val")
      .then(($identifier) => {
        const value = $identifier.text();
        console.log(value);
        expect(value).to.equal("8")
      })
  });
});
