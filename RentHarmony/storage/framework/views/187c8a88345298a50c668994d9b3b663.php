
<?php $__env->startSection('content'); ?>
    <section id="billboard" class="overflow-hidden">

      <button class="button-prev">
        <i class="icon icon-chevron-left"></i>
      </button>
      <button class="button-next">
        <i class="icon icon-chevron-right"></i>
      </button>
      <div class="swiper main-swiper">
        <div class="swiper-wrapper">
          <div class="swiper-slide" style="background-image: url(<?php echo e(asset('customer/images/ban1.jpg')); ?>);background-repeat: no-repeat;background-size: cover;background-position: center;">
            <div class="banner-content">
              <div class="container">
                <div class="row">
                  <div class="col-md-6">
                    <h2 class="banner-title" style="color:white">New Arrivals</h2>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu feugiat amet, libero ipsum enim pharetra hac.</p>
                    <div class="btn-wrap">
                      <a href="shop.html" class="btn btn-light btn-medium d-flex align-items-center" tabindex="0">Shop it now <i class="icon icon-arrow-io"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="swiper-slide" style="background-image: url(<?php echo e(asset('customer/images/ban2.jpg')); ?>);background-repeat: no-repeat;background-size: cover;background-position: center;">
            <div class="banner-content">
              <div class="container">
                <div class="row">
                  <div class="col-md-6">
                    <h2 class="banner-title" style="color:white">New Collection</h2>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu feugiat amet, libero ipsum enim pharetra hac.</p>
                    <div class="btn-wrap">
                      <a href="shop.html" class="btn btn-light btn-light-arrow btn-medium d-flex align-items-center" tabindex="0">Shop it now <i class="icon icon-arrow-io"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="featured-products" class="product-store padding-large">
  <div class="container">
    <div class="section-header d-flex flex-wrap align-items-center justify-content-between">
      <h2 class="section-title">Featured Products</h2>            
      <div class="btn-wrap">
        <a href="shop.html" class="d-flex align-items-center">View all products <i class="icon icon-arrow-io"></i></a>
      </div>            
    </div>
    <div class="swiper product-swiper overflow-hidden">
      <div class="swiper-wrapper">

        <div class="swiper-slide">
          <div class="product-item">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product1.jpg')); ?>" alt="Acoustic Guitar" class="product-image">
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
              <span class="item-price text-primary">$40.00</span>
            </div>
          </div>
        </div>

        <div class="swiper-slide">
          <div class="product-item">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product2.jpg')); ?>" alt="Digital Keyboard" class="product-image">
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
              <span class="item-price text-primary">$38.00</span>
            </div>
          </div>
        </div>

        <div class="swiper-slide">
          <div class="product-item">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product3.jpg')); ?>" alt="Electric Drum Set" class="product-image">
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
              <span class="item-price text-primary">$44.00</span>
            </div>
          </div>
        </div>

        <div class="swiper-slide">
          <div class="product-item">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product4.jpg')); ?>" alt="Violin" class="product-image">
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
              <span class="item-price text-primary">$33.00</span>
            </div>
          </div>
        </div>

      </div>
    </div>
    <div class="swiper-pagination"></div>
  </div>
</section>

    <section id="subscribe" class="padding-large">
      <div class="container">
        <div class="row">
          <div class="block-text col-md-6">
            <div class="section-header">
              <h2 class="section-title">Get 25% off Discount Coupons</h2>
            </div>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Dictumst amet, metus, sit massa posuere maecenas. At tellus ut nunc amet vel egestas.</p>
          </div>
          <div class="subscribe-content col-md-6">
            <form id="form" class="d-flex justify-content-between">
              <input type="text" name="email" placeholder="Enter your email addresss here">
              <button class="btn btn-dark">Subscribe Now</button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <section id="selling-products" class="product-store bg-light-grey padding-large">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">Best selling products</h2>
    </div>

    <div class="tab-content">
      <div id="all" data-tab-content class="active">
        <div class="row d-flex flex-wrap">
          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product5.jpg')); ?>" alt="Guitar" class="product-image">
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
              <img src="<?php echo e(asset('customer/images/product9.jpg')); ?>" alt="Drum" class="product-image">
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
                <a href="single-product.html">Drum Set</a>
              </h3>
              <div class="item-price text-primary">$35.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product7.jpg')); ?>" alt="Violin" class="product-image">
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
              <div class="item-price text-primary">$35.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product8.jpg')); ?>" alt="Keyboard" class="product-image">
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
              <div class="item-price text-primary">$30.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product10.jpg')); ?>" alt="Saxophone" class="product-image">
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
              <div class="item-price text-primary">$40.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product11.jpg')); ?>" alt="Trumpet" class="product-image">
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
                <a href="single-product.html">Trumpet</a>
              </h3>
              <div class="item-price text-primary">$30.00</div>
            </div>
          </div>

          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product12.jpg')); ?>" alt="Flute" class="product-image">
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
                <a href="single-product.html">Flute</a>
              </h3>
              <div class="item-price text-primary">$40.00</div>
            </div>
          </div>
          <div class="product-item col-lg-3 col-md-6 col-sm-6">
            <div class="image-holder">
              <img src="<?php echo e(asset('customer/images/product1.jpg')); ?>" alt="Flute" class="product-image">
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
                <a href="single-product.html">Violin</a>
              </h3>
              <div class="item-price text-primary">$40.00</div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</section>


    <section id="testimonials" class="padding-large no-padding-bottom">
      <div class="container">
        <div class="reviews-content">
          <div class="row d-flex flex-wrap">
            <div class="col-md-2">
              <div class="review-icon">
                <i class="icon icon-right-quote"></i>
              </div>
            </div>
            <div class="col-md-8">
              <div class="swiper testimonial-swiper overflow-hidden">
                <div class="swiper-wrapper">
                  <div class="swiper-slide">
                    <div class="testimonial-detail">
                      <p>“Dignissim massa diam elementum habitant fames. Id nullam pellentesque nisi, eget cursus dictumst pharetra, sit. Pulvinar laoreet id porttitor egestas dui urna. Porttitor nibh magna dolor ultrices iaculis sit iaculis.”</p>
                      <div class="author-detail">
                        <div class="name">By Maggie Rio</div>
                      </div>
                    </div>
                  </div>
                  <div class="swiper-slide">
                    <div class="testimonial-detail">
                      <p>“Dignissim massa diam elementum habitant fames. Id nullam pellentesque nisi, eget cursus dictumst pharetra, sit. Pulvinar laoreet id porttitor egestas dui urna. Porttitor nibh magna dolor ultrices iaculis sit iaculis.”</p>
                      <div class="author-detail">
                        <div class="name">By John Smith</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="swiper-arrows">
                <button class="prev-button">
                  <i class="icon icon-arrow-left"></i>
                </button>
                <button class="next-button">
                  <i class="icon icon-arrow-right"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    

    <section id="instagram" class="padding-large">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Follow our instagram</h2>
        </div>
        <p>Our official Instagram account <a href="#">@ultras</a> or <a href="#">#ultras_clothing</a>
        </p>
        <div class="row d-flex flex-wrap justify-content-between">
          <div class="col-lg-2 col-md-4 col-sm-6">
            <figure class="zoom-effect">
              <img src="<?php echo e(asset('customer/images/insta-image1.jpg')); ?>"alt="instagram" class="insta-image">
              <i class="icon icon-instagram"></i>
            </figure>
          </div>
          <div class="col-lg-2 col-md-4 col-sm-6">
            <figure class="zoom-effect">
              <img src="<?php echo e(asset('customer/images/insta-image2.jpg')); ?>"alt="instagram" class="insta-image">
              <i class="icon icon-instagram"></i>
            </figure>
          </div>
          <div class="col-lg-2 col-md-4 col-sm-6">
            <figure class="zoom-effect">
              <img src="<?php echo e(asset('customer/images/insta-image3.jpg')); ?>"alt="instagram" class="insta-image">
              <i class="icon icon-instagram"></i>
            </figure>
          </div>
          <div class="col-lg-2 col-md-4 col-sm-6">
            <figure class="zoom-effect">
              <img src="<?php echo e(asset('customer/images/insta-image4.jpg')); ?>"alt="instagram" class="insta-image">
              <i class="icon icon-instagram"></i>
            </figure>
          </div>
          <div class="col-lg-2 col-md-4 col-sm-6">
            <figure class="zoom-effect">
              <img src="<?php echo e(asset('customer/images/insta-image5.jpg')); ?>"alt="instagram" class="insta-image">
              <i class="icon icon-instagram"></i>
            </figure>
          </div>
          <div class="col-lg-2 col-md-4 col-sm-6">
            <figure class="zoom-effect">
              <img src="<?php echo e(asset('customer/images/insta-image6.jpg')); ?>"alt="instagram" class="insta-image">
              <i class="icon icon-instagram"></i>
            </figure>
          </div>
        </div>          
      </div>
    </section>

    <section id="shipping-information">
      <hr>
      <div class="container">
        <div class="row d-flex flex-wrap align-items-center justify-content-between">
          <div class="col-md-3 col-sm-6">
            <div class="icon-box">
              <i class="icon icon-truck"></i>
              <h4 class="block-title">
                <strong>Free shipping</strong> Over $200
              </h4>
            </div>
          </div>
          <div class="col-md-3 col-sm-6">
            <div class="icon-box">
              <i class="icon icon-return"></i>
              <h4 class="block-title">
                <strong>Money back</strong> Return within 7 days
              </h4>
            </div>
          </div>
          <div class="col-md-3 col-sm-6">
            <div class="icon-box">
              <i class="icon icon-tags1"></i>
              <h4 class="block-title">
                <strong>Buy 4 get 5th</strong> 50% off
              </h4>
            </div>
          </div>
          <div class="col-md-3 col-sm-6">
            <div class="icon-box">
              <i class="icon icon-help_outline"></i>
              <h4 class="block-title">
                <strong>Any questions?</strong> experts are ready
              </h4>
            </div>
          </div>
        </div>
      </div>
      <hr>
    </section>
 <?php $__env->stopSection(); ?>

   
<?php echo $__env->make('layouts.customermaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Customer/customerhome.blade.php ENDPATH**/ ?>