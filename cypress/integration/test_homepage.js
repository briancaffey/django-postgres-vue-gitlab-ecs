describe('Test visit homepage', function() {
  it("can visit the homepage", function() {
    cy.visit("/");
    cy.contains("Verbose Equals True");
  });
});
