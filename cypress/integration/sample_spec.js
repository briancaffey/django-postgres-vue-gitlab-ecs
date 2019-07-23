describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    cy.visit('http://backend/api/hello-world')
  })
})