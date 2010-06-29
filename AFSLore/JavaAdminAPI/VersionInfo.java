/*
 * @(#)VersionInfo.java	1.0 6/29/2001
 *
 * Copyright (c) 2001 International Business Machines Corp.
 * All rights reserved.
 *
 * This software has been released under the terms of the IBM Public
 * License.  For details, see the LICENSE file in the top-level source
 * directory or online at http://www.openafs.org/dl/license10.html
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package org.openafs.jafs;

import java.util.Date;

/**
 * Class providing static methods for retrieving version information specific to
 * the JNI library.
 * <BR><BR>
 *
 * <!--Example of how to use class-->
 * The following is a simple example of how to use the
 * <code>VersionInfo</code> class.
 * <PRE>
 * import org.openafs.jafs.VersionInfo;
 * ...
 * public class ...
 * {
 *   ...
 *   public static void main(String[] args) throws Exception
 *   {
 *     System.out.println("Attributes of the jafs native library:");
 *     System.out.println("\tDescription:\t" + VersionInfo.getDescription());
 *     System.out.println("\tCompile Date:\t" + VersionInfo.getCompileDate());
 *     System.out.println("\tVersion Number:\t" + VersionInfo.getBuildNumber());
 *   }
 *   ...
 * }
 * </PRE>
 *
 */
public final class VersionInfo
{
  /*-------------------------------------------------------------------------*/

  // No constructors, this is strictly a static class

  /*-------------------------------------------------------------------------*/


  ///////////////// accessors ///////////////////////

  /**
   * Returns the date, in the form of a {@link java.util.Date} object,
   * representing the compile-time of the native library.
   *
   * @see java.util.Date
   * @exception Exception   If an error occurs in the native code
   */
  public static final Date getBuildDate() throws Exception
  {
    return new Date(getBuildTime());
  }

  /**
   * Returns the version, in the form of "<version number>.<build number>",
   * representing the full version and build revision of the native library.
   *
   * @see #getVersion()
   * @see #getBuildNumber()
   * @exception Exception   If an error occurs in the native code
   */
  public static final String getFullVersion() throws Exception
  {
    return getVersion() + "." + getBuildNumber();
  }

  /////////////// native methods ////////////////////

  /**
   * Returns the date, in the form of a long value of milliseconds since 
   * "epoch", representing the compile-time of the native library.
   *
   * @see #getBuildTime
   * @exception Exception   If an error occurs in the native code
   */
  protected static final native long getBuildTime() throws Exception;

  /**
   * Returns the compile-time description of the native library.
   *
   * @exception Exception  If an error occurs in the native code
   */
  public static final native String getDescription() throws Exception;

  /**
   * Returns the build number of the native library.
   *
   * @exception Exception  If an error occurs in the native code
   */
  public static final native int getBuildNumber() throws Exception;

  /**
   * Returns the version number of the native library.
   *
   * @exception Exception  If an error occurs in the native code
   */
  public static final native String getVersion() throws Exception;

  /**
   * Returns the description of the platform that built the native library.
   *
   * @exception Exception  If an error occurs in the native code
   */
  public static final native String getBuildPlatform() throws Exception;
}
