
<?php $__env->startSection('content'); ?>

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Category Insert</h4>
                  <p class="card-description">
                    Insert your Category Information
                  </p>
                  <form action="<?php echo e(route('update_subcat',$subcat->subcatid)); ?>" method="post" enctype="multipart/form-data">
                     <?php echo csrf_field(); ?>
                    <div class="form-group">
                      <label for="exampleInputName1"> Subcategory Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="subcategoryname" value="<?php echo e($subcat->subcatname); ?>">
                    </div>

                    <div class="form-group">
                      <label for="exampleInputName1"> Image</label>
                      <img src="<?php echo e(asset('/uploads/' . $subcat->subimage)); ?>" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;">
                    </div>
                    <input type="hidden" class="form-control" id="exampleInputName1" placeholder="Name" name="oldimage" value="<?php echo e($subcat->subimage); ?>">

                    <input type="file" name="subimage" class="focus:shadow-primary-outline dark:bg-slate-850 dark:text-white text-sm leading-5.6 ease block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 outline-none transition-all placeholder:text-gray-500 focus:border-blue-500 focus:outline-none" /> <br> <br>
                    
                    <button type="submit" class="btn btn-primary mr-2">Submit</button>
                   
                  </form>
                   <?php if(session('success')): ?>
                  <script>
                    alert('<?php echo e(session('success')); ?>')
                  </script>
                  <?php endif; ?>
                </div>
              </div>
            </div>

            <?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/updatesubcategory.blade.php ENDPATH**/ ?>