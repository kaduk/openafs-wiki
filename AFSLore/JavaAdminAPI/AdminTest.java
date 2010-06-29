import org.openafs.jafs.ErrorTable;
import java.io.*;
import java.util.*;

/**
 * A common error testing class for the native methods
 */

public class AdminTest
{
  Properties properties;
  String cellName = null;
  String username = null;
  String password = null;

  org.openafs.jafs.Cell   cellHandle;
  org.openafs.jafs.Token  token;

  /*
    static
    {
    try {
    System.loadLibrary("pwd");
    } catch (Exception e) {
    // Ignore
    }
    }
  */

  AdminTest() throws Exception
  {
    InputStream in = new FileInputStream("adminTest.properties");
    if (in == null) throw new FileNotFoundException("adminTest.properties");
    properties = new Properties();
    properties.load(in);
    cellName = getProperty("cellName", cellName);
    //username = getProperty("username", username);
    //password = getProperty("password", password);
  }
  private String getProperty(String name, String dflt)
  {
    String p = properties.getProperty(name);
    return (p == null) ? dflt : p;
  }
  private int getProperty(String name, int dflt)
  {
    String p = properties.getProperty(name);
    if (p == null) {
      return dflt;
    } else {
      try {
        return Integer.parseInt(p);
      } catch (Exception e) {
        return dflt;
      }
    }
  }

  private void authenticate() throws IOException
  {
    try {
      System.out.println("  [user: " + username + "@" + cellName + "]");
      token = new org.openafs.jafs.Token( username, password, cellName );
      cellHandle = new org.openafs.jafs.Cell( token );
    } catch ( org.openafs.jafs.AFSException e ) {
      System.out.println( "Unexpected Exception\n  Error: " + ErrorTable.getMessage(e.getErrorCode()) + 
                          "\n  Cell: " + cellName + "\n  Username: " + username);
      return;
    }
  }

  private void listCell() throws Exception
  {
    try {
      System.out.println("======================================");
      System.out.println("LISTING CELL INFO");
      System.out.println("Total Number of Users: " + cellHandle.getUserCount());
      System.out.println("Total Number of Groups: " + cellHandle.getGroupCount());
      System.out.println("Total Number of Servers: " + cellHandle.getServerCount());
      System.out.println("======================================");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listUser(String name) throws Exception
  {
    if (name == null) {
      System.out.println("Name is null!");
      return;
    }
    org.openafs.jafs.User[] users = cellHandle.getUsers();
    try {
      System.out.println("Searching for user: " + name + "...");
      for (int i = 0; i < users.length; i++) {
        if (name.equals(users[i].getName())) {
          System.out.println("User found!\n");
          //System.out.println(users[i].getInfo());
          System.out.println(users[i].toString());
          System.out.println("Membership: " + users[i].getGroupMembershipCount());
          System.out.println("Groups Owned: " + users[i].getGroupsOwnedCount());
          return;
        }
      }
      System.out.println("User '" + name + "' could not be found!");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listUsers() throws Exception
  {
    org.openafs.jafs.User[] users = cellHandle.getUsers();
    try {
      System.out.println("======================================");
      System.out.println("LISTING USERS");
      for (int i = 0; i < users.length; i++) {
        System.out.println("User " + i + " = " + users[i].getName());
      }
      System.out.println("======================================");
      System.out.println("Total Number of Users: " + users.length);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listGroup(String name) throws Exception
  {
    if (name == null) {
      System.out.println("Name is null!");
      return;
    }
    org.openafs.jafs.Group[] groups = cellHandle.getGroups();
    try {
      System.out.println("Searching for group: " + name + "...");
      for (int i = 0; i < groups.length; i++) {
        if (name.equals(groups[i].getName())) {
          System.out.println("Group found!\n");
          groups[i].refresh();
          //System.out.println(groups[i].getInfo());
          System.out.println(groups[i].toString());
          System.out.println("Membership: " + groups[i].getMembershipCount());
          return;
        }
      }
      System.out.println("Group '" + name + "' could not be found!");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listGroups() throws Exception
  {
    org.openafs.jafs.Group[] groups = cellHandle.getGroups();
    try {
      System.out.println("======================================");
      System.out.println("LISTING GROUPS");
      for (int i = 0; i < groups.length; i++) {
        System.out.println("Group " + i + " = " + groups[i].getName());
      }
      System.out.println("======================================");
      System.out.println("Total Number of Groups: " + groups.length);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listGroupsX() throws Exception
  {
    org.openafs.jafs.Group[] groups = cellHandle.getGroups();
    try {
      System.out.println("======================================");
      System.out.println("LISTING GROUPS");
      for (int i = 0; i < groups.length; i++) {
        System.out.println("Group " + i + " = " + groups[i].getName());
      }
      System.out.println("======================================");
      System.out.println("Total Number of Groups: " + groups.length);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listServer(String name) throws Exception
  {
    if (name == null) {
      System.out.println("Name is null!");
      return;
    }
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("Searching for server: " + name + "...");
      for (int i = 0; i < servers.length; i++) {
        if (name.equals(servers[i].getName())) {
          System.out.println("Server found!\n");
          //System.out.println(servers[i].getInfo());
          System.out.println(servers[i].toString());
          System.out.println("# of Partition: " + servers[i].getPartitionCount());
          System.out.println("# of Admins: " + servers[i].getAdminCount());
          System.out.println("# of Keys: " + servers[i].getKeyCount());
          System.out.println("# of Processes: " + servers[i].getProcessCount());
          System.out.println("# of IP Addresses: " + servers[i].getIPAddresses().length);
          for (int x = 0; x < servers[i].getIPAddresses().length; x++) {
            System.out.println(" -> IP " + x + ": " + servers[i].getIPAddresses()[x]);
          }
          return;
        }
      }
      System.out.println("Server '" + name + "' could not be found!");
    } catch (org.openafs.jafs.AFSException e) {
      System.out.println("ERROR: " + ErrorTable.getMessage(e.getErrorCode()));
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listServers() throws Exception
  {
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("======================================");
      System.out.println("LISTING SERVERS");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("Server " + i + " = " + servers[i].toString());
      }
      System.out.println("======================================");
      System.out.println("Total Number of Servers: " + servers.length);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }


  private void listPartition(String name) throws Exception
  {
    if (name == null) {
      System.out.println("Name is null!");
      return;
    }
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("Searching for partition: " + name + "...");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("  Server " + i + " = " + servers[i].getName());
        if (!servers[i].isFileServer() || servers[i].isBadFileServer()) {
          System.out.println("  (not a file server)");
        } else {
          org.openafs.jafs.Partition[] partitions = servers[i].getPartitions();
          for (int p = 0; p < partitions.length; p++) {
            if (name.equals(partitions[p].getName())) {
              System.out.println("Partition found!\n");
              //System.out.println(partitions[p].getInfo());
              System.out.println(partitions[p].toString());
              System.out.println("Volume count: " + partitions[i].getVolumeCount());
            }
          }
        }
      }
      System.out.println("Done");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listPartitions() throws Exception
  {
    int n = 0;
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("======================================");
      System.out.println("LISTING PARTITIONS");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("Server " + i + " = " + servers[i].getName());
        if (!servers[i].isFileServer() || servers[i].isBadFileServer()) {
          System.out.println("  (not a file server)");
        } else {
          org.openafs.jafs.Partition[] partitions = servers[i].getPartitions();
          n += partitions.length;
          for (int p = 0; p < partitions.length; p++) {
            System.out.println("  Partition " + p + " = " + partitions[p].toString());
          }
        }
      }
      System.out.println("======================================");
      System.out.println("Total Number of Servers: " + servers.length);
      System.out.println("Total Number of Partitions: " + n);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  /*
    private void enumeratePartitions(String serverName, int start, int end) throws Exception
    {
    int i = 1;
    org.openafs.jafs.Server server = cellHandle.getServer(serverName);
    try {
    System.out.println("======================================");
    System.out.println("ENUMERATING PARTITIONS FROM " + start + " to " + end);
    Enumeration e = server.getPartitionEnumeration();

    i = start;
    while (e.hasMoreElements()) {
    System.out.println(" " + i + " -> " + e.nextElement());
    i++;
    //if (i >= end) break;
    }

    System.out.println("======================================");
    } catch (Exception e) {
    e.printStackTrace();
    }
    }
  */

  private void listVolume(String name) throws Exception
  {
    if (name == null) {
      System.out.println("Name is null!");
      return;
    }
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("Searching for volume: " + name + "...");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("  Server " + i + " = " + servers[i].getName());
        if (!servers[i].isFileServer() || servers[i].isBadFileServer()) {
          System.out.println("  (not a file server)");
        } else {
          org.openafs.jafs.Partition[] partitions = servers[i].getPartitions();
          for (int p = 0; p < partitions.length; p++) {
            System.out.println("    Partition " + p + " = " + partitions[p].getName());
            org.openafs.jafs.Volume[] volumes = partitions[p].getVolumes();
            for (int v = 0; v < volumes.length; v++) {
              if (name.equals(volumes[v].getName())) {
                System.out.println("        Volume found!\n");
                //System.out.println(volumes[v].getInfo());
                System.out.println(volumes[v].toString());
                System.out.println("Quota: " + volumes[v].getQuota());
              }
            }
          }
        }
      }
      System.out.println("Done");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listVolumes() throws Exception
  {
    int nP = 0;
    int nV = 0;
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("======================================");
      System.out.println("LISTING PARTITIONS");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("Server " + i + " = " + servers[i].getName());
        if (!servers[i].isFileServer() || servers[i].isBadFileServer()) {
          System.out.println("  (not a file server)");
        } else {
          org.openafs.jafs.Partition[] partitions = servers[i].getPartitions();
          nP += partitions.length;
          for (int p = 0; p < partitions.length; p++) {
            System.out.println("  Partition " + p + " = " + partitions[p].getName());
            org.openafs.jafs.Volume[] volumes = partitions[p].getVolumes();
            nV += volumes.length;
            for (int v = 0; v < volumes.length; v++) {
              System.out.println("    Volume " + v + " = " + volumes[v].getName());
            }
          }
        }
      }
      System.out.println("======================================");
      System.out.println("Total Number of Servers: " + servers.length);
      System.out.println("Total Number of Partitions: " + nP);
      System.out.println("Total Number of Volumes: " + nV);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  /*
    private void enumerateVolumes(String serverName, String partitionName, int start, int length) throws Exception
    {
    int i = 1;
    int n = 0;
    org.openafs.jafs.Server server = cellHandle.getServer(serverName);
    org.openafs.jafs.Partition partition = server.getPartition(partitionName);
    try {
    System.out.println("======================================");
    System.out.println("ENUMERATING PARTITIONS FROM " + start + " to " + (start + length));
    Enumeration e = partition.getVolumeEnumeration(start);

    i = start;
    while (e.hasMoreElements()) {
    System.out.println(" " + i + " -> " + e.nextElement());
    i++;
    n++;
    if (n >= length) break;
    }

    System.out.println("======================================");
    } catch (Exception e) {
    e.printStackTrace();
    }
    }
  */

  private void listProcess(String name) throws Exception
  {
    if (name == null) {
      System.out.println("Name is null!");
      return;
    }
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("Searching for process: " + name + "...");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("  Server " + i + " = " + servers[i].getName());
        org.openafs.jafs.Process[] processes = servers[i].getProcesses();
        for (int p = 0; p < processes.length; p++) {
          if (name.equals(processes[p].getName())) {
            System.out.println("Process found!\n");
            //System.out.println(processes[p].getInfo());
            System.out.println(processes[p].toString());
          }
        }
      }
      System.out.println("Done");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listProcesses() throws Exception
  {
    int n = 0;
    org.openafs.jafs.Server[] servers = cellHandle.getServers();
    try {
      System.out.println("======================================");
      System.out.println("LISTING PROCESSES");
      for (int i = 0; i < servers.length; i++) {
        System.out.println("Server " + i + " = " + servers[i].getName());
        org.openafs.jafs.Process[] processes = servers[i].getProcesses();
        n += processes.length;
        for (int p = 0; p < processes.length; p++) {
          System.out.println("  Process " + p + " = " + processes[p].getName());
        }
      }
      System.out.println("======================================");
      System.out.println("Total Number of Servers: " + servers.length);
      System.out.println("Total Number of Processes: " + n);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listACL(String path) throws Exception
  {
    try {
      System.out.println("======================================");
      System.out.println("LISTING ACL for: \n\t" + path);

      token.klog();
      org.openafs.jafs.ACL acl = new org.openafs.jafs.ACL(path);
      System.out.println(acl.toString());

      System.out.println("======================================");
    } catch (org.openafs.jafs.AFSException e) {
      System.out.println("AFS Error: " + e.getMessage());
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void setACL(String path) throws Exception
  {
    try {
      System.out.println("======================================");
      System.out.println("SETTING ACL for: \n\t" + path);

      token.klog();

      org.openafs.jafs.ACL acl = new org.openafs.jafs.ACL(path);
      System.out.println(acl.toString());

      org.openafs.jafs.ACL.Entry entry = new org.openafs.jafs.ACL.Entry( username, 29 );
      acl.addPositiveEntry(entry);

      System.out.println("Adding ACL entry: " + entry + "\n");
      System.out.println("ACL after modifications:");
      System.out.println(acl.toString());

      System.out.println("======================================");
    } catch (org.openafs.jafs.AFSException e) {
      System.out.println("AFS Error: " + e.getMessage());
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void listDir(String path) throws Exception
  {
    try {
      System.out.println("======================================");
      System.out.println("LISTING Directory for: \n\t" + path);

      token.klog();

      org.openafs.jafs.File file = new org.openafs.jafs.File(path);
      String[] e = file.list();
      if ( e == null ) {
        System.out.println( file.getErrorMessage() );
      } else {
        for (int i = 0; i < e.length; i++) {
          System.out.println(e[i]);
        }
      }

      System.out.println("======================================");
    } catch (org.openafs.jafs.AFSSecurityException e) {
      System.out.println("AFS Security Error: " + e.getMessage());
    } catch (org.openafs.jafs.AFSException e) {
      System.out.println("AFS Error: " + e.getMessage());
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void setUserGroupQuota() throws Exception
  {
    org.openafs.jafs.User user = cellHandle.getUser( username );
    try {
      System.out.println("======================================");
      System.out.println("SETTING GROUP QUOTA FOR " + user.getName());
      user.setGroupCreationQuota(-1);
      user.setGroupCreationQuota(20);
      user.setGroupCreationQuota(0);
      System.out.println("======================================");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void salvage(String name, String serverName, String partitionName) throws Exception
  {
    org.openafs.jafs.Server server = cellHandle.getServer(serverName);
    org.openafs.jafs.Partition partition = server.getPartition(partitionName);
    org.openafs.jafs.Volume volume = partition.getVolume(name);
    try {
      System.out.println("======================================");
      System.out.println("SALVAGING VOLUME " + volume.getName());
      volume.salvage();
      System.out.println("======================================");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void release(String name, String serverName, String partitionName) throws Exception
  {
    org.openafs.jafs.Server server = cellHandle.getServer(serverName);
    org.openafs.jafs.Partition partition = server.getPartition(partitionName);
    org.openafs.jafs.Volume volume = partition.getVolume(name);
    try {
      System.out.println("======================================");
      System.out.println("RELEASING VOLUME " + volume.getName());
      volume.release();
      System.out.println("======================================");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void createReadOnly(String name, String serverName, String partitionName) throws Exception
  {
    org.openafs.jafs.Server server = cellHandle.getServer(serverName);
    org.openafs.jafs.Partition partition = server.getPartition(partitionName);
    org.openafs.jafs.Volume volume = partition.getVolume(name);
    try {
      System.out.println("======================================");
      System.out.println("CREATING READ-ONLY REPLICA OF VOLUME " + volume.getName());
      //volume.createReadOnly(cellHandle.getServer(server), cellHandle.getPartition(server, partition));
      //volume.create( cellHandle, vosHandle, -1, newVolumeName, 0 );
      volume.createReadOnly(partition);
      System.out.println("======================================");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void createBackup(String name, String serverName, String partitionName) throws Exception
  {
    org.openafs.jafs.Server server = cellHandle.getServer(serverName);
    org.openafs.jafs.Partition partition = server.getPartition(partitionName);
    org.openafs.jafs.Volume volume = partition.getVolume(name);
    try {
      System.out.println("======================================");
      System.out.println("CREATING BACKUP REPLICA OF VOLUME " + volume.getName());
      volume.createBackup();
      System.out.println("======================================");
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  /**
   * execute:
   * takes in String representing a system command, executes it,
   * and waits for it to finish.
   *
   * throws IOException
   */
  private void execute( String command ) throws IOException
  {
    //System.out.println( "Executing: " + command );
    java.lang.Process proc = Runtime.getRuntime().exec( command );
    //      System.out.println( command );
    try {
      proc.waitFor();
    } catch ( InterruptedException e ) {
      throw new IOException( "Interrupted system command: " + command );
    }
  }

  private void printVersionInfo() throws Exception
  {
    System.out.println("JAFS native library build information:");
    System.out.println("\tDescription:    " + org.openafs.jafs.VersionInfo.getDescription());
    System.out.println("\tBuild Platform: " + org.openafs.jafs.VersionInfo.getBuildPlatform());
    System.out.println("\tBuild Time:     " + org.openafs.jafs.VersionInfo.getBuildDate());
    System.out.println("\tBuild Number:   " + org.openafs.jafs.VersionInfo.getBuildNumber());
    System.out.println("\tBuild Version:  " + org.openafs.jafs.VersionInfo.getVersion());
    System.out.println("\tFull Version:   " + org.openafs.jafs.VersionInfo.getFullVersion());
  }

  /**
   * Get password from native library 
   */
  //private static native String getNativePassword();

  private static String getPassword() throws IOException
  {
    String pwd = "";
    MaskingThread mt = new MaskingThread( "Please enter your AFS password: " );
    Thread t = new Thread( mt );
    t.start();

    while (true) {
      char c = (char)System.in.read();
      mt.stopMasking();
      if ( c == '\r' ) {
        c = (char) System.in.read();
        if ( c == '\n' ) {
          break;
        } else {
          continue;
        }
      } else if ( c == '\n' ) {
        break;
      } else {
        pwd += c;
      }
    }
    return pwd;
  }

  private static String getUsername()
  {
    System.out.print("Please enter your AFS username: ");
    BufferedReader r = new BufferedReader( new InputStreamReader(System.in) );
    try {
      return r.readLine();
    } catch (Exception e) {
      System.out.println("Error trying to read your username.");
      System.exit(1);
    }
    return null;
  }

  private static void printUsage()
  {
    System.out.println("Usage:");
    System.out.println("  AdminTest [auth] [cell] [user] [group] [server]");
    System.out.println("            [partition] [volume] [key] [process]");
    System.out.println("");
    System.out.println("  AdminTest [list users]      [list user <username>]");
    System.out.println("            [list groups]     [list group <group name>]");
    System.out.println("            [list servers]    [list server <server name>]");
    System.out.println("            [list partitions] [list partition <partition name>]");
    System.out.println("            [list volumes]    [list volume <volume name>]");
    System.out.println("            [list processes]  [list process <process name>]");
    System.out.println("            [list cell]");
    System.out.println("            [list dir <path>]");
    System.out.println("            [list acl <path>]");
    System.out.println("            [set  acl <path>]");
    System.out.println("            [enum partitions <server> <start> <length>]");
    System.out.println("            [enum volumes <server> <partition> <start> <length>]");
    System.out.println("            [vol salvage <volume name> <server> <partition>]");
    System.out.println("            [vol backup <volume name> <server> <partition>]");
    System.out.println("            [vol release <volume name> <server> <partition>]");
    System.out.println("            [vol replicate <volume name> <server> <partition>]");
    System.out.println("");
    System.out.println("            -v or -version     Display version of JAFS library");
    System.out.println("");
    System.out.println("            -u <username>");
    System.out.println("            -p <password>");
    System.out.println("");
    System.out.println("Example:");
    System.out.println("  AdminTest list users -u admin -p testpass");
    System.out.println("\nie: AdminTest cell\nThe above example will run the AdminTest program,\ntesting 'cell' functionality.");
  }
  public static void main(String[] args) throws Exception
  {
    AdminTest at = new AdminTest();
    try {
      for (int i = 0; i < args.length; i++) {
        if (args[i].startsWith("-h") || args[i].startsWith("h")) {
          printUsage();
          System.exit(0);
        } else if (args[i].equals("-u")) {
          i++;
          at.username = args[i];
        } else if (args[i].equals("-p")) {
          i++;
          at.password = args[i];
        } else if (args[i].equals("-g") || args[i].equals("--graphical")) {
          i++;
          PasswordPrompt p = new PasswordPrompt("AFS Admin Account");
            
          String[] info = new String[2];
          while ( p.isShowing() ) {
            Thread.sleep( 500 );
          }
          try {
            p.setUserInfo( info );
            at.username = info[0];
            at.password = info[1];
          } catch (Exception e2) {
            // Ignore
          }
        } else if (args[i].equals("-v") || args[i].equals("-version")) {
          at.authenticate();
          at.printVersionInfo();
          return;
        }
      }

      if ( at.username == null ) at.username = getUsername();
      if ( at.password == null ) at.password = getPassword();

      at.authenticate();

      if ( args.length > 0 ) run( at, args );

      while( true )
        {
          System.out.print("Command: ");
          BufferedReader r = new BufferedReader( new InputStreamReader(System.in) );
          try {
            run( at, split( r.readLine() ) );
          } catch (Exception e) {
            System.out.println("Error trying to read command.");
          }
        }
       
    } catch (ArrayIndexOutOfBoundsException e) {
      printUsage();
    }
  }
  private static void run( AdminTest at, String[] args ) throws Exception
  {
    try {
      for (int i = 0; i < args.length; i++) {
        if (args[i].equals("auth")) {
          System.out.println("not available");
          /*
            } else if (args[i].equals("enum")) {
            i++;
            if (args[i].equals("partitions")) {
            String serverName = args[i++];
            int start = Integer.parseInt(args[i++]);
            int end = Integer.parseInt(args[i++]);
            at.enumeratePartitions(serverName, start, end);
            } else if (args[i].equals("volumes")) {
            String serverName = args[++i];
            String partitionName = args[++i];
            int start = Integer.parseInt(args[++i]);
            int end = Integer.parseInt(args[++i]);
            at.enumerateVolumes(serverName, partitionName, start, end);
            }
          */
        } else if (args[i].equals("list")) {
          i++;
          if (args[i].equals("users")) {
            at.listUsers();
          } else if (args[i].equals("user")) {
            i++;
            at.listUser(args[i]);
          } else if (args[i].equals("groups")) {
            at.listGroups();
          } else if (args[i].equals("groupsx")) {
            at.listGroupsX();
          } else if (args[i].equals("group")) {
            i++;
            at.listGroup(args[i]);
          } else if (args[i].equals("servers")) {
            at.listServers();
          } else if (args[i].equals("server")) {
            i++;
            at.listServer(args[i]);
          } else if (args[i].equals("partitions")) {
            at.listPartitions();
          } else if (args[i].equals("partition")) {
            i++;
            at.listPartition(args[i]);
          } else if (args[i].equals("volumes")) {
            at.listVolumes();
          } else if (args[i].equals("volume")) {
            i++;
            at.listVolume(args[i]);
          } else if (args[i].equals("processes")) {
            at.listProcesses();
          } else if (args[i].equals("process")) {
            i++;
            at.listProcess(args[i]);
          } else if (args[i].equals("cell")) {
            at.listCell();
          } else if (args[i].equals("acl")) {
            i++;
            at.listACL(args[i]);
          } else if (args[i].equals("dir")) {
            i++;
            at.listDir(args[i]);
          }
        } else if (args[i].equals("set")) {
          i++;
          if (args[i].equals("user")) {
            i++;
            if (args[i].equals("group-quota")) {
              at.setUserGroupQuota();
            }
          } else if (args[i].equals("group")) {
          } else if (args[i].equals("acl")) {
            i++;
            at.setACL(args[i]);
          }
        } else if (args[i].equals("vol")) {
          i++;
          if (args[i].equals("salvage")) {
            i++;
            String name = args[i];
            i++;
            String server = args[i];
            i++;
            String partition = args[i];
            at.salvage(name, server, partition);
          } else if (args[i].equals("backup")) {
            i++;
            String name = args[i];
            i++;
            String server = args[i];
            i++;
            String partition = args[i];
            at.createBackup(name, server, partition);
          } else if (args[i].equals("release")) {
            i++;
            String name = args[i];
            i++;
            String server = args[i];
            i++;
            String partition = args[i];
            at.release(name, server, partition);
          } else if (args[i].equals("replicate")) {
            i++;
            String name = args[i];
            i++;
            String server = args[i];
            i++;
            String partition = args[i];
            at.createReadOnly(name, server, partition);
          }
        } else if (args[i].equals("cell")) {
          //at.testCell();
          System.out.println("Not Available");
        } else if (args[i].equals("user")) {
          //at.testUser();
          System.out.println("Not Available");
        } else if (args[i].equals("group")) {
          //at.testGroup();
          System.out.println("Not Available");
        } else if (args[i].equals("server")) {
          //at.testServer();
          System.out.println("Not Available");
        } else if (args[i].equals("partition") || args[i].equals("part")) {
          //at.testPartition();
          System.out.println("Not Available");
        } else if (args[i].equals("volume")) {
          //at.testVolume();
          System.out.println("Not Available");
        } else if (args[i].equals("key")) {
          //at.testKey();
          System.out.println("Not Available");
        } else if (args[i].equals("process") || args[i].equals("proc")) {
          //at.testProcess();
          System.out.println("Not Available");
        } else if (args[i].equals("h") || args[i].equals("help")) {
          printUsage();
        } else if (args[i].equals("q") || args[i].equals("quit")) {
          System.exit(0);
        } else if (args[i].equals("-u") || args[i].equals("-p")) {
          i++;
        } else if (args[i].equals("-g") || args[i].equals("--graphical")) {
          i++;
        } else {
          System.out.println("Invalid Argument: " + args[i]);
        }
      }
    } catch (ArrayIndexOutOfBoundsException e) {
      printUsage();
    }
  }

  private static String[] split( String str )
  {
    int i = 0;
    StringTokenizer st = new StringTokenizer(str);
    String[] tokens = new String[st.countTokens()];
    while (st.hasMoreTokens())  {
      tokens[i++] = st.nextToken().trim();
    }
    return tokens;
  }
  
  private static class MaskingThread extends Thread
  {
    private boolean stop = false;
    private int index;
    private String prompt;

    public MaskingThread( String prompt )
    {
      this.prompt = prompt;
    }
    public void run()
    {
      while ( !stop )
        {
          try {
            MaskingThread.sleep(1);
          } catch (InterruptedException e ) {
            e.printStackTrace();
          }
          if ( !stop ) {
            System.out.print("\r" + prompt );
          }
          System.out.flush();
        }    
    }
    public void stopMasking()
    {
      this.stop = true;
    }
  }

}
