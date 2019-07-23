describe('Visit test endpoint', function() {
  it('Visits test endpoint', function() {
    const resp = cy.request('http://nginxci/api/hello-world').its('body');
    console.log("response from debug api:");
    console.log(resp);
  })
});
