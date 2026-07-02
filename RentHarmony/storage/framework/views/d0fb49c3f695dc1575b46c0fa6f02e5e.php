
<?php $__env->startSection('content'); ?>
    <section id="featured-products" class="product-store ">
        <div class="container">
            <div class="section-header d-flex flex-wrap align-items-center justify-content-between">
                <h2 class="section-title">INSTRUMENT SUBCATEGORY</h2>
            </div>

            <div class="swiper product-swiper overflow-hidden">
                <div class="swiper-wrapper">
                    <?php $__empty_1 = true; $__currentLoopData = $subcategories; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $index => $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); $__empty_1 = false; ?>
                        <div class="swiper-slide">
                            <div class="product-item">
                                <div class="image-holder">
                                    <img src="<?php echo e(asset('/uploads/' . $d->subimage)); ?>" alt="Books" class="product-image"
                                        style="width:400px; height:300px;">
                                </div>
                                <div class="cart-concern">
                                    <div class="cart-button d-flex justify-content-between align-items-center">
                                         <a href="<?php echo e(route('customerinstview' , ['subcatid' => $d->subcatid])); ?>" class="btn-wrap cart-link d-flex align-items-center">
                                           EXPLORE MORE
</a>
                                       
                                    </div>
                                </div>
                                <div class="product-detail">
                                    <h3 class="product-title">
                                        <a href="single-product.html"><?php echo e($d->subcatname); ?></a>
                                    </h3>
                                    <span class="item-price text-primary"><br><br></span>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); if ($__empty_1): ?>
    <div class="col-12 text-center my-5">
        <div style="font-size: 80px;">🛒❌</div>
        <h4 class="text-muted mt-3">Sorry, no products found!</h4>
    </div>
                <?php endif; ?>

                </div>
            </div>

            <div class="swiper-pagination"></div>
        </div>
    </section>
<?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.customermaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Customer/customersubcatview.blade.php ENDPATH**/ ?>