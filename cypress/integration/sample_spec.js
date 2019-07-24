describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    cy.log("visiting nginx host");
    cy.request("http://backend:8000/api/hello-world");
    expect('A').to.not.equal('B');
    cy.visit("/");
    cy.log("response from debug api:");
    cy.log(resp);
  })
});
