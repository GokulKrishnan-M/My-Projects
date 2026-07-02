@extends('layouts.customermaster')
@section('content')

<section id="selling-products" class="product-store bg-light-grey">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">Best Selling Products</h2>
    </div>

    <div class="tab-content">
      <div id="all" data-tab-content class="active">
        <div class="row d-flex flex-wrap">

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product5.jpg')}}" alt="Guitar" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Acoustic Guitar</a>
              </h3>
              <div class="item-price text-primary">$40.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product9.jpg')}}" alt="Keyboard" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Digital Keyboard</a>
              </h3>
              <div class="item-price text-primary">$35.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product7.jpg')}}" alt="Drum" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Electronic Drum Set</a>
              </h3>
              <div class="item-price text-primary">$35.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product8.jpg')}}" alt="Violin" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Classic Violin</a>
              </h3>
              <div class="item-price text-primary">$30.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product10.jpg')}}" alt="Flute" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Silver Flute</a>
              </h3>
              <div class="item-price text-primary">$40.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product11.jpg')}}" alt="Saxophone" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Alto Saxophone</a>
              </h3>
              <div class="item-price text-primary">$30.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product12.jpg')}}" alt="Trumpet" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Golden Trumpet</a>
              </h3>
              <div class="item-price text-primary">$40.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="{{asset('customer/images/product1.jpg')}}" alt="Electric Guitar" class="product-image">
            </div>
            <div class="cart-concern">
              <div class="cart-button d-flex justify-content-between align-items-center">
                <button type="button" class="btn-wrap cart-link d-flex align-items-center">add to cart <i class="icon icon-arrow-io"></i></button>
                <button type="button" class="view-btn tooltip d-flex">
                  <i class="icon icon-screen-full"></i>
                  <span class="tooltip-text">Quick view</span>
                </button>
                <button type="button" class="wishlist-btn">
                  <i class="icon icon-heart"></i>
                </button>
              </div>
            </div>
            <div class="product-detail">
              <h3 class="product-title">
                <a href="single-product.html">Electric Guitar</a>
              </h3>
              <div class="item-price text-primary">$35.00</div>
            </div>
          </div>

        </div>
      </div>
    </div>
    <br><br>
</section>
@endsection
