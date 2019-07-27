describe('Test Login', function() {
  it("User can login through UI", function() {
    cy.visit("/");
    cy.get("#login").click();
    cy.get("#email").clear();
    cy.get("#email").type("admin@company.com");
    cy.get("#password").clear();
    cy.get("#password").type("password");
    cy.get("#login-btn").click();
    cy.wait(500) // wait for 2 seconds
    cy.getCookie('user-token').should('exist')
  });
});
