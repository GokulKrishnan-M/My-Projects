
<?php $__env->startSection('content'); ?>

<div class="col-lg-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Striped Table</h4>
                  <p class="card-description">
                    Add class <code>.table-striped</code>
                  </p>
                  <div class="table-responsive">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>
                            CUSTOMER NAME
                          </th>
                          <th>
                            INSTRUMENT NAME
                          </th>
                           <th>
                            BOOK DATE
                          </th>
                          <th>
                            VIEW MORE
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <?php $__currentLoopData = $cust; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $index => $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                            <tr>
                                <td><?php echo e($d->cust->custname); ?></td>
                               <td><?php echo e($d->inst->instname); ?></td>
                               <td><?php echo e($d->bookdate); ?></td>
                               <td>
                                    <a href="<?php echo e(route('viewmorebook', ['bookid' => $d->bookid])); ?>" class="btn btn-sm btn-primary" >View More</a>
                                </td>
                            </tr>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
</div>
</div>

            <?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/customerview.blade.php ENDPATH**/ ?>