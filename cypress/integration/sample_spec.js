describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    cy.log("visiting nginx host");
    const resp = cy.visit('http://nginx').its('body');
    cy.log("response from debug api:");
    cy.log(resp);
    expect('A').to.not.equal('B')
  })
});
