describe "app", (not-it) ->
  beforeEach ->
    browser! .navigateTo "/"

  it "should redirect to /view1 when hash/fragment is empty", ->
    expect(browser!location!url!) .toBe "/view1"
