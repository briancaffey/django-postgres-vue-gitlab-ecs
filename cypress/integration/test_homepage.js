describe('Test Login', function() {
  it("Can visit homepage", function() {
    cy.visit("/");
    cy.contains("Verbose Equals True");
  });
});
