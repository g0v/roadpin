# This file is copied to spec/ when you run 'rails generate rspec:install'
ENV["RAILS_ENV"] ||= 'test'
require File.expand_path("../../config/environment", __FILE__)
require 'rspec/rails'
require 'factory_girl'
require 'capybara/rspec'
require 'capybara/poltergeist'
require 'capybara-screenshot/rspec'
require 'webmock/rspec'
require 'vcr'

WebMock.disable_net_connect!(:allow_localhost => true)

driver = ENV['DRIVER'] || 'poltergeist'
#Capybara.default_driver = driver.to_sym
#Capybara.javascript_driver = :poltergeist
#Capybara.always_include_port = true
#Capybara.default_wait_time = 30

VCR.configure do |c|
  c.ignore_hosts '127.0.0.1', 'localhost'
  c.cassette_library_dir = 'spec/fixtures/vcr_cassettes'
  c.hook_into :webmock # or :fakeweb
end
# Requires supporting ruby files with custom matchers and macros, etc,
# in spec/support/ and its subdirectories.
Dir[Rails.root.join("spec/support/**/*.rb")].each {|f| require f}

RSpec.configure do |config|
  config.use_transactional_fixtures = true
  config.infer_base_class_for_anonymous_controllers = false
  config.order = "--seed 1234"
  config.mock_with :rspec

  config.include FactoryGirl::Syntax::Methods
end
