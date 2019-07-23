describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    cy.log("visiting nginx host");
    const resp = cy.visit('http://nginxci:80/about');
    cy.log("response from debug api:");
    cy.log(resp);
  })
});
