using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace Server
{
    class Program
    {
        static void Main(string[] args)
        {
            var serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            serverSocket.Bind(new IPEndPoint(IPAddress.Any, 41775));
            serverSocket.Listen(100);
            Console.WriteLine("[i] Listening on: " + IPAddress.Any + ":41775 (TCP)");
            var clientSockets = new System.Collections.Generic.List<Socket>();
            while (true)
            {
                var clientSocket = serverSocket.Accept();
                Console.WriteLine("[+] " + clientSocket.RemoteEndPoint + " connected");
                clientSockets.Add(clientSocket);
                var thread = new Thread(() =>
                {
                    int bytesReceived = 0;
                    var buffer = new byte[32768];
                    string data;
                    while (true)
                    {
                        data = "";
                        try
                        {
                            bytesReceived = clientSocket.Receive(buffer);
                        }
                        catch (System.Net.Sockets.SocketException)
                        {
                            Console.WriteLine("[-] " + clientSocket.RemoteEndPoint + " disconnected");
                            clientSockets.Remove(clientSocket);
                            clientSocket.Close();
                            break;
                        }
                        if (bytesReceived == 0)
                        {
                            Console.WriteLine("[-] " + clientSocket.RemoteEndPoint + " disconnected");
                            clientSockets.Remove(clientSocket);
                            clientSocket.Close();
                            break;
                        }

                        data = Encoding.UTF8.GetString(buffer, 0, bytesReceived);
                        foreach (var socket in clientSockets)
                        {
                            socket.Send(Encoding.UTF8.GetBytes(data));
                        }
                    }
                });
                thread.Start();
            }
        }
    }
}
