
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
                            SI.
                          </th>
                          <th>
                            CATEGORY NAME
                          </th>
                          <th>
                            IMAGE
                          </th>
                           <th>
                            DELETE
                          </th>
                           <th>
                            UPDATE
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                         <?php $__currentLoopData = $cat; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $index => $d): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                            <tr>
                                <td><?php echo e($index + 1); ?></td>
                                <td><?php echo e($d->catname); ?></td>
                                <td>
                                <img src="<?php echo e(asset('/uploads/' . $d->image)); ?>" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;"></td>
                                <td>
                                    <a href="<?php echo e(route('deletecat' , ['catid' => $d->catid])); ?>" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this Department?')">Delete</a>
                                </td>
                                <td>
                                    <a href="<?php echo e(route('updatecat' , ['catid' => $d->catid])); ?>" class="btn btn-sm btn-primary" >Edit</a>
                                </td>
                            </tr>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                      </tbody>
                    </table>
                     <?php if(session('success')): ?>
                  <script>
                    alert('<?php echo e(session('success')); ?>')
                  </script>
                  <?php endif; ?>
                  </div>
                  </div>
                  </div>
                  </div>
                
                </div>
              </div>
            </div>

            <?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.adminmaster', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/categoryview.blade.php ENDPATH**/ ?>