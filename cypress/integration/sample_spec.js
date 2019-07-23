describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    cy.log("visiting nginx host");
    const resp = cy.visit('http://nginxci').its('body');
    cy.log("response from debug api:");
    cy.log(resp);
  })
});
