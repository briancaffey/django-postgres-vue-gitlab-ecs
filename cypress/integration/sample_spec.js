describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    const resp = cy.request('http://backend:8000/api/hello-world').its('body');
    console.log("response from debug api:");
    console.log(resp);
  })
})