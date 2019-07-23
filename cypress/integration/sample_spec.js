describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    cy.visit('http://backend:8000/api/hello-world')
  })
})