describe('Test Login', function() {
  it('Finds the text of the homepage', function() {
    cy.visit("/");
  });
  it('Can query api through nginx proxy pass', function() {
    cy.request("/api/");
  })
});
