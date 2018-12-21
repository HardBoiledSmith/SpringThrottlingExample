package io.hbsmith;

import es.moki.ratelimitj.core.limiter.request.RequestLimitRule;
import es.moki.ratelimitj.core.limiter.request.RequestRateLimiter;
import es.moki.ratelimitj.inmemory.request.InMemorySlidingWindowRequestRateLimiter;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.Duration;

@Controller
public class HelloController {

    private final RequestRateLimiter rateLimiterJSP = new InMemorySlidingWindowRequestRateLimiter(
            RequestLimitRule.of(Duration.ofMinutes(1), 3));

    private final RequestRateLimiter rateLimiterAPI = new InMemorySlidingWindowRequestRateLimiter(
            RequestLimitRule.of(Duration.ofMinutes(1), 6));

    @RequestMapping(value = {"/"}, method = RequestMethod.GET)
    public String displayIndex() {
        return "index";
    }

    @RequestMapping(value = {"/jsp"}, method = RequestMethod.GET)
    public String displayJSP(HttpServletRequest request, ModelMap model) {
        String clientIp = request.getRemoteAddr();
        if (rateLimiterJSP.overLimitWhenIncremented("remote-ip:" + clientIp)) {
            return "too_many_requests";
        } else {
            model.addAttribute("message", "Hello JSP!");
            return "hello";
        }
    }

    @RequestMapping(value = {"/api"}, method = RequestMethod.GET)
    @ResponseBody
    public void displayAPI(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String clientIp = request.getRemoteAddr();
        if (rateLimiterAPI.overLimitWhenIncremented("remote-ip:" + clientIp)) {
            response.setStatus(429);
        } else {
            response.setStatus(200);
            response.setContentType("text/html;charset=UTF-8");
            PrintWriter out = response.getWriter();
            out.println("Hello REST API!");
        }
    }
}
