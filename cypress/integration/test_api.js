describe('Test API', function () {
  it("Can access a public API route", function () {
    cy.request("/api/")
      .its('body')
      .then((body) => {
        expect(body).to.deep.equal({"message": "Root"});
      });
  });
});