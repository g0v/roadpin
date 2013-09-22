describe "partial2", (not-it) ->
  beforeEach ->
    browser! .navigateTo "/"

  afterEach ->
  
  it "should redirect to /view1 when has/fragment is empty", ->
    expect(browser!location!url!) .toBe "/view1"
